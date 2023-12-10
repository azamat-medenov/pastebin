import pytest

from src.application.user.schemas.user import UserCreateDTO


@pytest.fixture
def create_user_schema():
    return UserCreateDTO(
        username='user12',
        email='user1@gmail.com',
        name='user12',
        password='user12password'
    )