import os
from typing import Any

import aioboto3
from dotenv import load_dotenv

load_dotenv()


class S3Singleton:
    __instance = None

    def __init__(self) -> None:
        self.client = aioboto3.Session(
            region_name=os.getenv("REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        ).client("s3")

    def __new__(cls, *args: Any, **kwargs: Any) -> "S3Singleton":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    @property
    def bucket_name(self) -> str:
        name = os.getenv("AWS_S3_BUCKET")
        if not name:
            raise ValueError("Could not get bucket name")
        return name


def s3() -> S3Singleton:
    return S3Singleton()
