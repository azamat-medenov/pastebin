from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.specification import Specification
from src.application.user.schemas.user import UserCreateDTO, UserDTO
from src.infrastructure.database.models.user import User


class UserRepo(Protocol):
    def __init__(self, session: AsyncSession):
        ...

    async def get_user(self, specification: Specification) -> User | None:
        ...

    async def is_user_exists(self, schema: UserCreateDTO) -> bool:
        ...

    async def create_user(self, schema: UserDTO) -> User:
        ...
