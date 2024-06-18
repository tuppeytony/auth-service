from http import HTTPStatus
from typing import Any

import pytest

from tests.functional.testdata.database_mapping import claims_data
from tests.functional.testdata.database_mapping import database_data


@pytest.mark.parametrize(
    ('request_data', 'expected_answer'),
    [
        (
            claims_data[0],
            {'status': HTTPStatus.OK, 'response': claims_data[0]},
        ),
        (
            claims_data[2],
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            claims_data[3],
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            claims_data[4],
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            claims_data[0],
            {'status': HTTPStatus.BAD_REQUEST},
        ),
        (
            claims_data[5],
            {'status': HTTPStatus.NOT_FOUND},
        ),
    ],
)
@pytest.mark.asyncio()
async def test_create_user_claims(
    authenticated_http_client: Any,
    get_user_by_email: Any,
    request_data: dict,
    expected_answer: dict,
) -> None:
    """Тестирование создания свойств для пользователя."""
    user = await get_user_by_email(database_data[0]['email'])
    if fake_user_id := request_data.get('user_id'):
        request = {
            **request_data,
            **{'user_id': fake_user_id},
        }
    else:
        request = {
            **request_data,
            **{'user_id': str(user.auth_user_id)},
        }
    response = await authenticated_http_client.post(
        '/user-claim',
        json=request,
    )
    status_code = response.status_code
    assert expected_answer['status'] == status_code
    if request_response := request_data.get('response'):
        assert request_response == response
