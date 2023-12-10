import typing
from datetime import datetime
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationError,
    field_validator
)
if typing.TYPE_CHECKING:
    from src.application.user.schemas.user import UserDTO


class EntryDTO(BaseModel):
    id: uuid.UUID
    text: str
    link_to_cloud: str
    link: str
    date_created: datetime
    expire_on: datetime
    author_fk: str

    model_config = ConfigDict(from_attributes=True)


class EntryWithAuthorDTO(EntryDTO):
    author: 'UserDTO'


class CreateEntry(BaseModel):
    text: str
    expire_on: datetime

    @field_validator('expire_on')
    @classmethod
    def check_expire_date(cls, value: datetime) -> datetime:
        if value < datetime.now():
            raise ValidationError('expire date must not be over')
        return value


