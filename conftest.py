import asyncio

from typing import Any
from typing import Generator

import pytest


pytest_plugins = (
    'tests.functional.project_fixtures.db_fixtures',
    'tests.functional.project_fixtures.client_fixtures',
)


@pytest.fixture(scope='session')
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    """."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
