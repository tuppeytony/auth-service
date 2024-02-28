from http import HTTPStatus
from typing import Any

import pytest

from tests.functional.settings import tests_settings
from tests.functional.testdata.database_mapping import database_data


@pytest.mark.parametrize(
    ('request_data', 'expected_answer'),
    [
        (
            {'email': 'test@mail.ru', 'password': 'qwerty'},
            {'status': HTTPStatus.CREATED},
        ),
        (
            {'email': 'test@mail.ru', 'password': '1111'},
            {'status': HTTPStatus.BAD_REQUEST, 'response': {'detail': 'Пользователь с таким email уже существует.'}},
        ),
        (
            {'email': 'fizzbizz', 'password': 'qwerty'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'response': {
                'detail': [
                    {
                        'type': 'value_error',
                        'loc': [
                            'body',
                            'email',
                        ],
                        'msg': ('value is not a valid email address: The email address is not valid. '
                                'It must have exactly one @-sign.'),
                        'input': 'fizzbizz',
                        'ctx': {
                            'reason': 'The email address is not valid. It must have exactly one @-sign.',
                        },
                    },
                ],
            },
            },

        ),
    ],
)
@pytest.mark.asyncio()
async def test_registration(
    request_api_post: Any,
    request_data: dict,
    expected_answer: dict,
) -> None:
    """Тесты регистрации."""
    response, status_code = await request_api_post('/registration', request_data)
    assert expected_answer['status'] == status_code
    if request_response := request_data.get('response'):
        assert request_response == response


@pytest.mark.parametrize(
    ('request_data', 'expected_answer'),
    [
        (
            database_data[0],
            {'status': HTTPStatus.OK},
        ),
        (
            {'email': 'lol@mail.ru', 'password': '4321'},
            {'status': HTTPStatus.FORBIDDEN, 'response': {'detail': 'Неправильный пароль'}},
        ),
        (
            {'email': 'notexist@mail.ru', 'password': '4321'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'response': {'detail': 'Пользователь не существует'}},
        ),
    ],
)
@pytest.mark.asyncio()
async def test_login(
    request_api_post: Any,
    request_data: dict,
    expected_answer: dict,
) -> None:
    """Тесты для логина."""
    response, status_code = await request_api_post('/login', request_data)
    assert expected_answer['status'] == status_code
    if request_response := request_data.get('response'):
        assert request_response == response


@pytest.mark.parametrize(
    ('request_data', 'expected_answer'),
    [
        (
            None,
            {'status': HTTPStatus.UNAUTHORIZED},
        ),
        (
            database_data[0],
            {'status': HTTPStatus.OK},
        ),
    ],
)
@pytest.mark.asyncio()
async def test_refresh(
    request_api_post: Any,
    expected_answer: dict,
    request_data: dict | None,
    authenticated_http_client: Any,
) -> None:
    """Тесты для обновления токена."""
    _, status_code = await request_api_post('/refresh', request_data)
    if request_data:
        refresh_response = await authenticated_http_client.post(f'{tests_settings.service_api_url}/refresh')
        status_code = refresh_response.status_code
    assert expected_answer['status'] == status_code


@pytest.mark.parametrize(
    ('request_data', 'expected_answer'),
    [
        (
            None,
            {'status': HTTPStatus.UNAUTHORIZED},
        ),
        (
            database_data[0],
            {'status': HTTPStatus.OK},
        ),
    ],
)
@pytest.mark.asyncio()
async def test_logout(
    authenticated_http_client: Any,
    request_data: dict | None,
    expected_answer: dict,
    http_client: Any,
) -> None:
    """Тестирование логаута."""
    response = await http_client.delete(f'{tests_settings.service_api_url}/logout')
    if request_data:
        response = await authenticated_http_client.delete(f'{tests_settings.service_api_url}/logout')
    assert response.status_code == expected_answer['status']
