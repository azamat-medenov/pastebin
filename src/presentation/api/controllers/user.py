import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from src.application.user.schemas.token import Token
from src.presentation.api.providers.stub import Stub
from src.infrastructure.database.repo.user import UserRepo
from src.application.user.schemas.user import (
    UserOutDTO, UserCreateDTO
)
from src.application.user.user import (
    _create_user,
    _get_user,
    authenticate_user,
    get_current_user
)

user_router = APIRouter(
    prefix='/users',
    tags=['users']
)


@user_router.post(
    '/', status_code=status.HTTP_201_CREATED)
async def create_user(
        user: UserCreateDTO,
        session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]
) -> UserOutDTO:
    return await _create_user(UserRepo(session), user)


@user_router.get('/{user_id}')
async def get_user(
        user_id: uuid.UUID,
        session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]
) -> UserOutDTO:
    return await _get_user(UserRepo(session), user_id)


@user_router.post(
    '/login',
    response_model=Token,
    status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]
) -> dict[str, str]:
    token = await authenticate_user(
        form_data.username,
        UserRepo(session),
        form_data.password
    )
    return {'token_type': 'bearer', 'access_token': token}