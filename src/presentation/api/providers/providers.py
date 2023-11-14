from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI

from src.presentation.api.providers.stub import Stub
from src.infrastructure.database.factory import get_async_session


def setup_providers(app: FastAPI) -> None:

    app.dependency_overrides[Stub(AsyncSession)] = get_async_session
