from typing import Protocol, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.specification import Specification
from src.infrastructure.database.models.user import User
from src.application.user.schemas.user import UserCreateDTO, UserDTO


class UserRepo(Protocol):
    def __init__(self, session: AsyncSession): ...

    async def get_user(self, specification: Specification) -> User: ...

    async def is_user_exists(self, schema: UserCreateDTO) -> bool: ...

    async def create_user(self, schema: UserDTO) -> User: ...
