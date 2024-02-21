__all__ = (
    'BaseSchema',
)

from typing import Any

import orjson

from pydantic import BaseModel


def orjson_dumps(value: Any, *, default: Any) -> Any:
    """Декодирование из bites в unicode."""
    return orjson.dumps(value, default=default).decode()


class BaseSchema(BaseModel):
    """Настройка для базовых классов схем."""

    class Config:
        """."""

        json_loads = orjson.loads
        json_dumps = orjson_dumps
        from_attributes = True
