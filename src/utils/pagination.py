from typing import Annotated

from fastapi import Query


class Paginator:
    """Пагинатор."""

    def __init__(
        self,
        limit: Annotated[int, Query(description='Количество записей', ge=1, le=100)] = 20,
        offset: Annotated[int, Query(description='Страница', ge=0)] = 0,
    ):
        self.limit = limit
        self.offset = offset
