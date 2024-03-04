import os
from datetime import datetime, timedelta, timezone

import aioboto3
import pytest
from httpx import AsyncClient

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


def get_mock_s3():
    return MockS3Singleton()


app.dependency_overrides[Stub(S3Singleton)] = get_mock_s3


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


@pytest.fixture()
async def s3_client():
    return aioboto3.Session().client("s3", endpoint_url=os.getenv("AWS_ENDPOINT_URL"))


async def test_create_entry(
    s3_client, ac: AsyncClient, erase_users, create_user_schema
):
    access_token = await test_login(ac, create_user_schema, erase_users)
    res = await ac.post(
        "/entry",
        json={
            "text": "testtext",
            "expire_on": (
                datetime.now(tz=timezone(timedelta(hours=6))) + timedelta(hours=6)
            ).isoformat(),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 201
