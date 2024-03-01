import typing
import uuid
from datetime import datetime, timedelta, timezone

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, field_validator

if typing.TYPE_CHECKING:
    from src.application.user.schemas.user import UserDTO

UTC_6 = timezone(timedelta(hours=6))


class EntryDTO(BaseModel):
    id: uuid.UUID
    text: str
    date_created: datetime
    expire_on: datetime
    author_fk: str

    model_config = ConfigDict(from_attributes=True)


class EntryWithAuthorDTO(EntryDTO):
    author: "UserDTO"


class CreateEntry(BaseModel):
    text: str
    expire_on: datetime

    @field_validator("expire_on")
    @classmethod
    def check_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise RequestValidationError("Expire date must have timezone")
        return value

    @field_validator("expire_on")
    @classmethod
    def check_expire_date(cls, value: datetime) -> datetime:
        if value < datetime.now(UTC_6) or datetime.now(UTC_6) + timedelta(7) < value:
            raise RequestValidationError(
                "Expire date must not be over or more than a week"
            )
        return value.astimezone(tz=UTC_6).replace(tzinfo=None)
