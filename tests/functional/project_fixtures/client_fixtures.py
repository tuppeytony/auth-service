from typing import AsyncGenerator

import pytest_asyncio

from asgi_lifespan import LifespanManager
from httpx import ASGITransport
from httpx import AsyncClient

from src.main import app
from tests.functional.settings import tests_settings


@pytest_asyncio.fixture()
async def http_client() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для HTTP клиента."""
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app),  # type: ignore[arg-type]
            base_url=tests_settings.service_api_url,
        ) as client:
            yield client
