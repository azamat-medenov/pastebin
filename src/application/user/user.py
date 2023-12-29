import os
import uuid
from datetime import timedelta, datetime
from typing import TypeAlias, Annotated

from dotenv import load_dotenv
from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from email_validator import validate_email, EmailNotValidError
from jose import jwt, JWTError

from src.application.services.specification import (
    IDSpecification,
    EmailSpecification,
    UsernameSpecification,)
from src.application.services.uuid7 import uuid7
from src.application.services.hash_password import (
    hash_password, bcrypt_context)
from src.infrastructure.database.interfaces.user import UserRepo
from src.application.user.schemas.user import (
    UserCreateDTO, UserDTO, UserOutDTO)
from src.application.user.exceptions import UnAuthorizedError

UsernameOrEmail: TypeAlias = str

load_dotenv()

JWT_EXPIRES = timedelta(hours=1)
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='users/login')


async def _get_user(
        repo: UserRepo,
        user_id: uuid.UUID) -> UserOutDTO:
    user = await repo.get_user(IDSpecification(user_id))
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
        user = await repo.get_user(UsernameSpecification(login))
    else:
        user = await repo.get_user(EmailSpecification(login))
    if user is not None:
        return UserDTO.model_validate(user)


def create_access_token(
        username: str, user_id: uuid.UUID, expires: timedelta) -> str:
    return jwt.encode({
        'username': username,
        'exp': datetime.now() + expires,
        'id': str(user_id)
    }, SECRET_KEY, ALGORITHM)


async def authenticate_user(
        login: UsernameOrEmail,
        repo: UserRepo,
        password: str) -> str:
    user = await check_login(login, repo)
    if user is not None and bcrypt_context.verify(
            password,
            user.hashed_password):
        return create_access_token(user.username, user.id, JWT_EXPIRES)

    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail='BAD CREDENTIALS')


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)]
) -> uuid.UUID:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('username')
        user_id = payload.get('id')
        if username is None or user_id is None:
            raise JWTError
        return user_id
    except JWTError:
        raise UnAuthorizedError()


