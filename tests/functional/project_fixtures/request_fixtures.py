from typing import Any
from typing import Callable

import pytest

from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from src.main import app
from tests.functional.settings import tests_settings


@pytest.fixture()
def registration() -> Callable[[Any, Any], Any]:
    """Фикстура для тестов регистрации."""
    async def inner(endpoint: str, request_data: dict) -> tuple[Any, int]:
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url=tests_settings.service_api_url) as client:
                response = await client.post(endpoint, json=request_data)
            body = response.json()
            status_code = response.status_code
        return body, status_code
    return inner
