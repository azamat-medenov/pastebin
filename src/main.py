import uvicorn
from fastapi import FastAPI


def main() -> FastAPI:
    app = FastAPI()
    return app


def run() -> None:
    uvicorn.run('src:main', reload=True)


if __name__ == "__main__":
    run()
