import typing
import uuid
from typing import List


from pydantic import BaseModel, Field, EmailStr, ConfigDict

if typing.TYPE_CHECKING:
    from src.application.entry.schemas.entry import EntrySchema


class UserBaseSchema(BaseModel):
    username: str = Field(max_length=20, min_length=6)
    email: EmailStr
    name: str = Field(max_length=20, min_length=6)

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(UserBaseSchema):
    password: str = Field(max_length=30, min_length=8)


class UserOutSchema(UserBaseSchema):
    id: uuid.UUID


class UserSchema(UserOutSchema):
    hashed_password: str
    entries: List['EntrySchema'] = []


class UserWithPasswordSchema(UserSchema, UserCreateSchema):
    pass
