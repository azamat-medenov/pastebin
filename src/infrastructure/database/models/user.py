import typing
import uuid
from typing import List

from src.infrastructure.database.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.application.services.uuid7 import uuid7

if typing.TYPE_CHECKING:
    from src.infrastructure.database.models.entry import Entry


class User(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid7)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    name: Mapped[str] = mapped_column(String(25))
    email: Mapped[str]
    hashed_password: Mapped[str]

    entries: Mapped[List['Entry']] = relationship(back_populates='author', cascade='all, delete-orphan')

    def __str__(self) -> str:
        return f'{self.username=}, {self.name=}'
