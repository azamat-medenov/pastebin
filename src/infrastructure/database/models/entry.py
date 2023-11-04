import typing
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base import Base


if typing.TYPE_CHECKING:
    from src.infrastructure.database.models.user import User

class Entry(Base):
    __tablename__ = 'entry'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    text: Mapped[str]
    link_to_cloud: Mapped[str]
    link: Mapped[str]
    date_created: Mapped[datetime] = mapped_column(d)
    expire_on: Mapped[datetime]
    author_fk: Mapped[str] = mapped_column(ForeignKey('user.username'))

    author: Mapped['User'] = relationship(back_populates='entry', cascade='all, delete-orphan')

    def __str__(self) -> str:
        return f'{self.id=}, {self.author=}'
