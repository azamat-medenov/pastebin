from datetime import datetime
from typing import Any, Type
from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.entry.schemas.entry import CreateEntry
from src.infrastructure.database.models.entry import Entry


class EntryRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model: Type[Entry] = Entry

    async def get_entry(self, key: UUID) -> Entry | None:
        query = select(self.model).where(
            self.model.id == key, self.model.expire_on > datetime.now()
        )
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def create_entry(self, schema: CreateEntry, user_id: UUID) -> Any:
        stmt = (
            insert(self.model)
            .values(expire_on=schema.expire_on, author_fk=user_id)
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.one()
