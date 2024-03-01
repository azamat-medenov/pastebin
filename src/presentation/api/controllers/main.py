from fastapi import FastAPI

from src.presentation.api.controllers.entry import entry_router
from src.presentation.api.controllers.user import user_router


def setup_controllers(app: FastAPI) -> None:
    app.include_router(user_router)
    app.include_router(entry_router)
