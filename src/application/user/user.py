import os
import uuid

from typing import Type

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.application.services.uuid7 import uuid7
from src.application.services.hash_password import hash_password
from src.infrastructure.database.interfaces.user import UserRepo
from src.application.user.schemas.user import (
    UserCreateSchema, UserSchema, UserOutSchema)


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

# oauth2_bearer = OAuth


async def _get_user(
        repo: Type[UserRepo],
        user_id: uuid.UUID,
        session: AsyncSession) -> UserOutSchema:
    res = await repo(session).get_user(user_id)
    if res is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='USER DOES NOT EXIST')

    return UserOutSchema(
        id=res.id,
        username=res.username,
        email=res.email,
        name=res.name,
    )


async def _create_user(
        repo: Type[UserRepo],
        user: UserCreateSchema,
        session: AsyncSession) -> UserOutSchema:
    if await repo(session).is_user_exists(user):
        raise HTTPException(status.HTTP_409_CONFLICT, detail='USERNAME OR EMAIL ALREADY TAKEN')

    new_user = UserSchema(
        id=uuid7(),
        hashed_password=hash_password(user.password),
        **user.model_dump()
    )
    res = await repo(session).create_user(new_user)
    return UserOutSchema(**res)
