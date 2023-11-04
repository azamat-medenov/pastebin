import typing
from typing import List

from pydantic import BaseModel

if typing.TYPE_CHECKING:
    from src.application.schemas.entry import EntrySchema
class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    entries: List['EntrySchema'] = []

