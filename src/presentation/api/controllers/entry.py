from typing import Annotated
from uuid import UUID

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.entry.schemas.entry import CreateEntry
from src.application.user.user import get_current_user
from src.infrastructure.database.repo.entry import EntryRepo
from src.infrastructure.s3.commands import s3_entry_upload, s3_get_entry
from src.infrastructure.s3.factory import S3Singleton
from src.presentation.api.providers.stub import Stub

entry_router = APIRouter(prefix="/entry", tags=["entry"])

load_dotenv()


@entry_router.post("", status_code=status.HTTP_201_CREATED)
async def create_entry(
    entry: CreateEntry,
    user_id: Annotated[UUID, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
    s3: Annotated[S3Singleton, Depends(Stub(S3Singleton))],
) -> UUID:
    res_entry = await EntryRepo(db_session).create_entry(entry, user_id)
    await s3_entry_upload(s3.bucket_name, entry.text, res_entry.id, s3.client)
    return res_entry.id


@entry_router.get("", status_code=status.HTTP_200_OK)
async def get_entry(
    entry_id: UUID,
    db_session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
    s3: Annotated[S3Singleton, Depends(Stub(S3Singleton))],
) -> str:
    res_entry = await EntryRepo(db_session).get_entry(entry_id)
    if res_entry is None:
        raise HTTPException(status_code=404, detail="No entry with that id was found")

    return await s3_get_entry(bucket=s3.bucket_name, key=entry_id, s3_client=s3.client)
