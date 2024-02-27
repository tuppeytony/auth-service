from typing import Any
from typing import Callable

import pytest

from httpx import AsyncClient


@pytest.fixture()
def registration(http_client: AsyncClient) -> Callable[[Any, Any], Any]:
    """Фикстура для тестов регистрации."""
    async def inner(endpoint: str, request_data: dict) -> tuple[Any, int]:
        response = await http_client.post(endpoint, json=request_data)
        body = response.json()
        status_code = response.status_code
        return body, status_code
    return inner
