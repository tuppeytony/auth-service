from datetime import date
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .base import Base


class AuthUser(Base):
    """Таблица аутентификационного пользователя."""

    __tablename__ = 'auth_user'

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = generate_password_hash(password)

    auth_user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_email_confirmed: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    creation_date: Mapped[date] = mapped_column(Date(), nullable=False, default=date.today)
    user_enabled: Mapped[bool] = mapped_column(default=True, nullable=False)

    def check_user_hash_password(self, password: str) -> bool:
        """Проверка хэша пароля пользователя."""
        return check_password_hash(self.password, password)


# TODO: добавить ip адреса пользователей, user agent
class UserSession(Base):
    """Модель сессий пользователя."""

    __tablename__ = 'user_session'

    def __init__(
        self,
        auth_user_id: UUID,
        logout_time: Optional[datetime] = None,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
    ):
        self.auth_user_id = auth_user_id
        self.logout_time = logout_time
        self.user_agent = user_agent
        self.ip_address = ip_address

    session_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    login_time = Column(DateTime(), default=datetime.now, nullable=False)
    logout_time = Column(DateTime(), nullable=True)
    auth_user_id: Mapped[UUID] = mapped_column(ForeignKey('auth_user.auth_user_id', ondelete='CASCADE'), nullable=False)
    user_agent: Mapped[Optional[str]] = mapped_column(String(400), nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(15), nullable=False)
