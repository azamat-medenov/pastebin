import typing
import uuid
from typing import List

from pydantic import BaseModel, Field, EmailStr, ConfigDict

if typing.TYPE_CHECKING:
    from src.application.entry.schemas.entry import EntryDTO


class Login(BaseModel):
    email_or_username: str
    password: str


class UserBaseDTO(BaseModel):
    username: str = Field(max_length=20, min_length=6)
    email: EmailStr
    name: str = Field(max_length=20, min_length=6)

    model_config = ConfigDict(from_attributes=True)


class UserCreateDTO(UserBaseDTO):
    password: str = Field(max_length=30, min_length=8)


class UserOutDTO(UserBaseDTO):
    id: uuid.UUID


class UserDTO(UserOutDTO):
    hashed_password: str


class UserRelDTO(UserDTO):
    entries: List['EntryDTO'] = []
