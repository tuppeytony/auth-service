from schemas import BaseSchema


class TokenSchema(BaseSchema):
    """Схема для токена."""

    access_token: str
    refresh_token: str
