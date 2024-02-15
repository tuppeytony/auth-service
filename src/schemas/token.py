from pydantic import BaseModel
from pydantic import ConfigDict


class TokenSchema(BaseModel):
    """Схема для токена."""

    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
