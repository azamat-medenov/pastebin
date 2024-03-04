from datetime import datetime, timedelta, timezone

import pytest


@pytest.fixture
def entry():
    return {
        "text": "testtext",
        "expire_on": (
            datetime.now(tz=timezone(timedelta(hours=6))) + timedelta(hours=6)
        ).isoformat(),
    }
