from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class BaseUserEntity(BaseModel):
    """Базовая сущность для пользователя."""

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseUserEntity):
    """Сущность для аутентификации пользователя."""

    email: EmailStr
    password: str
