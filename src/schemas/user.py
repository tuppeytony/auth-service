from pydantic import EmailStr

from .base_schema import BaseSchema


class UserLoginSchema(BaseSchema):
    """Сущность для аутентификации пользователя."""

    email: EmailStr
    password: str


class UserRegisterSchema(UserLoginSchema):
    """Сущность для регистрации пользователя."""

    pass


class UserRestorePasswordSchema(BaseSchema):
    """Схема для восстановления пароля."""

    email: EmailStr
