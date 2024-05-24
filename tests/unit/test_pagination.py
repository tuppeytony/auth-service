import pytest

from src.utils import Paginator


@pytest.mark.parametrize(
    ('init_data', 'expected_answer'),
    [
        (
            {'limit': 10, 'offset': 1},
            {'result': (10, 1)},
        ),
        (
            {},
            {'result': (20, 0)},
        ),
    ],
)
def test_pagination(
    init_data: dict,
    expected_answer: dict,
) -> None:
    """Тестирование пагинации."""
    paginator = Paginator(**init_data)
    limit, offset = expected_answer['result']
    assert paginator.limit == limit
    assert paginator.offset == offset
