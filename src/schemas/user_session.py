from datetime import date
from datetime import datetime

from pydantic import EmailStr
from pydantic import Field

from .base_schema import BaseSchema


class UserSessionSchema(BaseSchema):
    """Схема для истории пользователя."""

    login_time: datetime
    logout_time: datetime | None
    email: EmailStr
    is_email_confirmed: bool
    creation_date: date
    user_agent: str | None = Field(max_length=200)
    ip_address: str = Field(max_length=15)
