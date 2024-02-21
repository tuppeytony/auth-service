from pydantic import EmailStr

from schemas import BaseSchema


class UserLogin(BaseSchema):
    """Сущность для аутентификации пользователя."""

    email: EmailStr
    password: str


class UserRegister(UserLogin):
    """Сущность для регистрации пользователя."""

    pass


class UserRestorePassword(BaseSchema):
    """Схема для восстановления пароля."""

    email: EmailStr
