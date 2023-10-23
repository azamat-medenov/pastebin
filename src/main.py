import uvicorn
from fastapi import FastAPI


def main() -> FastAPI:
    app = FastAPI()
    return app


def run():
    uvicorn.run('src:main')


if __name__ == "__main__":
    run()
