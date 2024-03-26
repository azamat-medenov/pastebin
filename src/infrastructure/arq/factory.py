import os

from arq import cron
from arq.connections import RedisSettings
from dotenv import load_dotenv

from src.infrastructure.arq.expires_cron import delete_expired_entries

load_dotenv()


def at_every_x_hours(x: int, start: int = 0, end: int = 24) -> set[int]:
    return {*list(range(start, end, x))}


class WorkerSettings:
    cron_jobs = [
        cron(coroutine=delete_expired_entries, minute=0, hour=at_every_x_hours(1))
    ]
    redis_settings = RedisSettings(
        host=os.environ["REDIS_HOST"], port=int(os.environ["REDIS_PORT"])
    )
