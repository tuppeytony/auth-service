from datetime import date
from datetime import datetime

from pydantic import EmailStr

from .base_schema import BaseSchema


class UserSessionSchema(BaseSchema):
    """Схема для истории пользователя."""

    login_time: datetime
    logout_time: datetime | None
    email: EmailStr
    is_email_confirmed: bool
    creation_date: date
    user_agent: str | None
    ip_address: str
