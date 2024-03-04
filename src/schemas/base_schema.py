from pydantic import BaseModel
from pydantic import ConfigDict


class BaseSchema(BaseModel):
    """Настройка для базовых классов схем."""

    model_config = ConfigDict(from_attributes=True)
