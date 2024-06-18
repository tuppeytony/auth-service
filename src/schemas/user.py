from pydantic import EmailStr
from pydantic import Field

from .base_schema import BaseSchema


class UserLoginSchema(BaseSchema):
    """Сущность для аутентификации пользователя."""

    email: EmailStr
    password: str = Field(min_length=4)


class UserRegisterSchema(UserLoginSchema):
    """Сущность для регистрации пользователя."""

    pass


class UserRestorePasswordSchema(BaseSchema):
    """Схема для восстановления пароля."""

    email: EmailStr
