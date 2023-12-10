from typing import Type, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, or_

from src.application.services.specification import Specification
from src.application.user.schemas.user import (
    UserCreateDTO, UserDTO)
from src.infrastructure.database.models.user import User


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model: Type[User] = User

    async def get_user(
            self, specification: Specification) -> User:
        query = select(self.model).filter_by(
            **specification.is_specified()
        )
        res = await self.session.execute(query)
        return res.scalar_one()

    async def is_user_exists(self, schema: UserCreateDTO) -> bool:
        query = select(self.model).where(or_(
            self.model.username == schema.username,
            self.model.email == schema.email)
        )
        res = await self.session.execute(query)
        return res.first() is not None

    async def create_user(self, schema: UserDTO) -> Any:
        stmt = insert(self.model).values(
            id=schema.id,
            username=schema.username,
            name=schema.name,
            hashed_password=schema.hashed_password,
            email=schema.email
        ).returning(
            self.model.id,
            self.model.username,
            self.model.email,
            self.model.name)

        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.one()

    async def get_hashed_password(
            self, specification: Specification) -> str:
        query = (select(self.model.hashed_password).
                 filter_by(**specification.is_specified()))

        res = await self.session.execute(query)
        return res.scalar_one()


