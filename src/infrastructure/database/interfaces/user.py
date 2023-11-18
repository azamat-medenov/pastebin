import uuid
from typing import Protocol, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Row

from src.infrastructure.database.models.user import User
from src.application.user.schemas.user import UserCreateSchema, UserSchema


class UserRepo(Protocol):
    def __init__(self, session: AsyncSession): ...

    async def get_user(self, **fields: Any) -> User : ...

    async def is_user_exists(self, schema: UserCreateSchema) -> bool: ...

    async def create_user(self, schema: UserSchema) -> User: ...
