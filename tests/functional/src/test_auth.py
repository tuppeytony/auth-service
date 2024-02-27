from http import HTTPStatus
from typing import Any

import pytest


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
    registration: Any,
    request_data: dict,
    expected_answer: dict,
) -> None:
    """Тесты регистрации."""
    response, status_code = await registration('/registration', request_data)
    assert expected_answer['status'] == status_code
    if request_response := request_data.get('response'):
        assert request_response == response
