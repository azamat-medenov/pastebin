import pytest
from sqlalchemy import delete

from src.infrastructure.database.models import Entry, User
from tests.conftest import Base, test_engine


@pytest.fixture
async def erase_users():
    async with test_engine.begin() as conn:
        stmt1 = delete(Entry)
        stmt = delete(User)
        await conn.execute(stmt1)
        await conn.execute(stmt)


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
