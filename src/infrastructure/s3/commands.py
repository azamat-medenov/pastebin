from uuid import UUID

from types_aiobotocore_s3.client import S3Client


async def s3_entry_upload(
    bucket: str, text: str, key: UUID, s3_client: S3Client
) -> None:
    async with s3_client as s3:
        await s3.put_object(
            ACL="bucket-owner-full-control",
            Body=text,
            Bucket=bucket,
            ContentLength=len(text),
            ContentEncoding="UTF-8",
            Key=str(key) + ".txt",
        )


async def s3_get_entry(bucket: str, key: UUID, s3_client: S3Client) -> str:
    async with s3_client as s3:
        res = await s3.get_object(Bucket=bucket, Key=str(key) + ".txt")
        content = await res["Body"].read()
        return content.decode()
