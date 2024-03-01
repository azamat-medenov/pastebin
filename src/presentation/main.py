import uvicorn
from fastapi import FastAPI

from presentation.api.providers.imports import setup_imports
from src.presentation.api.controllers.main import setup_controllers
from src.presentation.api.providers.providers import setup_providers


def main() -> FastAPI:
    app = FastAPI()
    setup_imports()
    setup_controllers(app)
    setup_providers(app)
    return app


def run() -> None:
    uvicorn.run(r"main:main", reload=True, port=8000)


if __name__ == "__main__":
    run()
