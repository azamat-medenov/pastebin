import typing
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base import Base
from src.application.services.uuid7 import uuid7

if typing.TYPE_CHECKING:
    from src.infrastructure.database.models.user import User


class Entry(Base):
    __tablename__ = 'entry'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid7)
    text: Mapped[str]
    link_to_cloud: Mapped[str]
    link: Mapped[str]
    date_created: Mapped[datetime] = mapped_column(default=datetime.now())
    expire_on: Mapped[datetime]
    author_fk: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), nullable=False, index=True)

    author: Mapped['User'] = relationship(back_populates='entries')

    def __str__(self) -> str:
        return f'{self.id=}, {self.author=}'
