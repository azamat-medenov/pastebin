from typing import Type, TypeVar

from src.application.user.schemas.user import (
    UserBaseSchema,
    UserCreateSchema,
)
from src.infrastructure.database.models.user import User

US = TypeVar('US', bound=UserBaseSchema)


def user_to_pydantic(
        schema: Type[US],
        user: User,
        password: str | None = None
) -> US:
    fields = {}
    print(user.username)

    for field in schema.model_fields:
        if (password is not None and field
                == 'password' and issubclass(schema, UserCreateSchema)):
            fields['password'] = password
        else:
            fields[field] = user.__getattribute__(field)

    return schema(
        **fields
    )
