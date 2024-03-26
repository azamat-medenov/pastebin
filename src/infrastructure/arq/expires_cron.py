from typing import Any

from src.infrastructure.database.factory import SessionLocal
from src.infrastructure.database.repo.entry import EntryRepo
from src.infrastructure.s3.factory import S3Singleton


async def delete_expired_entries(*args: Any, **kwargs: Any) -> None:
    s3 = S3Singleton()
    async with SessionLocal() as db_session:
        entries = await EntryRepo(db_session).check_expires()
        if entries:
            async with s3.client as s3_client:
                res = await s3_client.delete_objects(
                    Bucket=s3.bucket_name,
                    Delete={
                        "Objects": [
                            {"Key": str(entry[0]) + ".txt"} for entry in entries
                        ]
                    },
                )
                print(res)
        await db_session.commit()
