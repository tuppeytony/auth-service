from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from werkzeug.security import generate_password_hash

from .base import Base


class AuthUser(Base):
    """Таблица аутентификационного пользователя."""

    __tablename__ = 'auth_user'

    def __init__(self, email: Column[str], password: str):
        self.email = email
        self.password = generate_password_hash(password)

    auth_user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_email_confirmed = Column(Boolean(), nullable=False, default=False)


class UserSession(Base):
    """Модель сессий пользователя."""

    __tablename__ = 'user_session'

    def __init__(self, login_time: Optional[datetime], logout_time: Optional[datetime], auth_user_id: UUID):
        self.login_time = login_time
        self.logout_time = logout_time
        self.auth_user_id = auth_user_id

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    login_time = Column(DateTime(), default=datetime.now)
    logout_time = Column(DateTime(), nullable=True)
    auth_user_id: Mapped[UUID] = mapped_column(ForeignKey('auth_user.auth_user_id', ondelete='CASCADE'), nullable=False)
