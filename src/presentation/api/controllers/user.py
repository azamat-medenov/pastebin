import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.api.providers.stub import Stub
from src.infrastructure.database.repo.user import UserRepo
from src.application.user.schemas.user import (
    UserOutSchema, UserCreateSchema)
from src.application.user.user import _create_user, _get_user

user_router = APIRouter(
    prefix='/users',
    tags=['users']
)


@user_router.post(
    '/', status_code=status.HTTP_201_CREATED)
async def create_user(
        user: UserCreateSchema,
        session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]
) -> UserOutSchema:
    return await _create_user(UserRepo, user, session)


@user_router.get('/{user_id}')
async def get_user(
        user_id: uuid.UUID,
        session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]
) -> UserOutSchema:
    return await _get_user(UserRepo, user_id, session)
