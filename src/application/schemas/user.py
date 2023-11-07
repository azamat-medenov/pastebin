import typing
import uuid
from typing import List

from pydantic import BaseModel

if typing.TYPE_CHECKING:
    from src.application.schemas.entry import EntrySchema


class UserSchema(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    name: str
    hashed_password: str
    entries: List['EntrySchema'] = []
