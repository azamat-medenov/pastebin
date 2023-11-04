import typing
from typing import List

from src.infrastructure.database.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
    from src.infrastructure.database.models.entry import Entry


class User(Base):
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String(25), primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    email: Mapped[str]
    password: Mapped[str]

    entries: Mapped[List['Entry']] = relationship(backref='author')

    def __str__(self) -> str:
        return f'{self.username=}, {self.name=}'
