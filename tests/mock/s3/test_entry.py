import os

import aioboto3
import pytest
from httpx import AsyncClient
from types_aiobotocore_s3.client import S3Client

from src.infrastructure.s3.factory import S3Singleton
from src.presentation.api.providers.stub import Stub
from src.presentation.main import main
from tests.integration.test_user_commands import test_login

app = main()


class MockS3Singleton:
    __instance = None

    def __init__(self) -> None:
        self.client = aioboto3.Session(
            region_name=os.getenv("REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        ).client(service_name="s3", endpoint_url=os.environ["AWS_ENDPOINT_URL"])

    def __new__(cls, *args, **kwargs) -> "S3Singleton":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    @property
    def bucket_name(self) -> str:
        name = os.getenv("AWS_S3_BUCKET")
        if not name:
            raise ValueError("Could not get bucket name")
        return name


@pytest.fixture()
async def s3_client():
    return MockS3Singleton().client


@pytest.fixture(scope="session")
async def mock_boto():
    from moto.server import ThreadedMotoServer

    server = ThreadedMotoServer()

    server.start()
    port = server._server.socket.getsockname()[1]
    os.environ["AWS_ENDPOINT_URL"] = f"http://127.0.0.1:{port}"

    yield
    del os.environ["AWS_ENDPOINT_URL"]
    server.stop()


@pytest.fixture(autouse=True, scope="session")
async def create_bucket(mock_boto):
    s3 = MockS3Singleton().client
    async with s3 as s3:
        await s3.create_bucket(
            Bucket=os.getenv("aws_s3_bucket"),
            CreateBucketConfiguration={
                "LocationConstraint": os.getenv("AWS_REGION_NAME")
            },
        )


app.dependency_overrides[Stub(S3Singleton)] = s3_client


async def test_create_entry(
    s3_client: S3Client, ac: AsyncClient, erase_users, create_user_schema, entry
):
    access_token = await test_login(ac, create_user_schema, erase_users)
    res = await ac.post(
        "/entry",
        json=entry,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    id = res.json()
    assert res.status_code == 201
    async with s3_client as s3:
        res = await s3.get_object(Bucket=os.getenv("AWS_S3_BUCKET"), Key=id + ".txt")
        content = await res["Body"].read()
        assert content.decode() == entry["text"]
    return id


async def test_get_entry(
    s3_client: S3Client, ac: AsyncClient, erase_users, create_user_schema, entry
):
    id = await test_create_entry(s3_client, ac, erase_users, create_user_schema, entry)
    res = await ac.get("/entry", params={"entry_id": id})
    assert res.status_code == 200
    assert res.json() == entry["text"]
