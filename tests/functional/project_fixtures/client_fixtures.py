from typing import Any
from typing import AsyncGenerator
from typing import Callable
from typing import Optional

import pytest
import pytest_asyncio

from asgi_lifespan import LifespanManager
from httpx import ASGITransport
from httpx import AsyncClient

from src.main import app
from tests.functional.settings import tests_settings
from tests.functional.testdata.database_mapping import database_data


@pytest_asyncio.fixture()
async def http_client() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для HTTP клиента."""
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app),  # type: ignore[arg-type]
        ) as client:
            yield client


@pytest_asyncio.fixture()
async def authenticated_http_client() -> AsyncGenerator[AsyncClient, None]:
    """Аутентифицированный клиент."""
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app)) as auth_client:  # type: ignore[arg-type]
            login_reques = await auth_client.post(f'{tests_settings.service_api_url}/login', json=database_data[0])
            await auth_client.aclose()
        async with AsyncClient(
            cookies=login_reques.cookies,
            transport=ASGITransport(app),  # type: ignore[arg-type]
        ) as client:
            yield client


@pytest.fixture()
def request_api_post(http_client: AsyncClient) -> Callable[[Any, Any], Any]:
    """Фикстура для тестов регистрации."""
    async def inner(endpoint: str, request_data: Optional[dict] = None) -> tuple[Any, int]:
        request_data = request_data or {}
        response = await http_client.post(f'{tests_settings.service_api_url}{endpoint}', json=request_data)
        body = response.json()
        status_code = response.status_code
        return body, status_code
    return inner
