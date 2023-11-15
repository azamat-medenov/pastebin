import pytest

from src.application.user.schemas.user import UserCreateSchema


@pytest.fixture
def create_user_schema():
    return UserCreateSchema(
        username='user12',
        email='user1@gmail.com',
        name='user12',
        password='user12password'
    )