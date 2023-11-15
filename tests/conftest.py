import asyncio
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from httpx import AsyncClient
from fastapi.testclient import TestClient

from src.presentation.api.providers.stub import Stub
from src.presentation.main import main
from src.infrastructure.database.models.base import Base

from tests.setup.env import (DB_USER_TEST,
                             DB_PASSWORD_TEST,
                             DB_HOST_TEST,
                             DB_NAME_TEST,
                             DB_PORT_TEST)


pytest_plugins = [
    "tests.fixtures.user",
    "tests.fixtures.db",
  ]


DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

test_engine = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)

Base.metadata.bind = test_engine

SessionTest = async_sessionmaker(bind=test_engine)

app = main()


async def override_get_session():
    async with SessionTest() as session:
        yield session


app.dependency_overrides[Stub(AsyncSession)] = override_get_session


@pytest.fixture
async def erase_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope='session')
async def prepare_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
