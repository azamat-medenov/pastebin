import os
import uuid

from typing import TypeAlias

from dotenv import load_dotenv
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from email_validator import validate_email, EmailNotValidError

from src.application.services.uuid7 import uuid7
from src.application.services.hash_password import (
    hash_password, bcrypt_context)
from src.infrastructure.database.interfaces.user import UserRepo
from src.application.user.schemas.user import (
    UserCreateDTO, UserDTO, UserOutDTO)

UsernameOrEmail: TypeAlias = str

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='users/token')


async def _get_user(
        repo: UserRepo,
        user_id: uuid.UUID) -> UserOutDTO:
    user = await repo.get_user(id=user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='USER DOES NOT EXIST')

    return UserOutDTO.model_validate(user)


async def _create_user(
        repo: UserRepo,
        user: UserCreateDTO) -> UserOutDTO:
    if await repo.is_user_exists(user):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail='USERNAME OR EMAIL ALREADY TAKEN')

    new_user = UserDTO(
        id=uuid7(),
        hashed_password=hash_password(user.password),
        **user.model_dump()
    )
    res = await repo.create_user(new_user)
    return UserOutDTO.model_validate(res)


async def check_login(
        login: UsernameOrEmail,
        repo: UserRepo) -> UserDTO | None:
    try:
        validate_email(login)
    except EmailNotValidError:
        user = await repo.get_user(username=login)
    else:
        user = await repo.get_user(email=login)
    if user is not None:
        return UserDTO.model_validate(user)


async def authenticate_user(
        login: UsernameOrEmail,
        repo: UserRepo,
        password: str) -> UserDTO:
    user = await check_login(login, repo)
    if user is not None and bcrypt_context.verify(
            user.hashed_password,
            password):
        return user

    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail='BAD CREDENTIALS')
