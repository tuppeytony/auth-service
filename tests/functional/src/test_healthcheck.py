from http import HTTPStatus
from typing import Any

import pytest

from tests.functional.settings import tests_settings


@pytest.mark.asyncio()
async def test_healthcheck(
    http_client: Any,
) -> None:
    """Тестирование хелфчека."""
    response = await http_client.get(f'{tests_settings.service_url}/healthcheck')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': 'ok'}
