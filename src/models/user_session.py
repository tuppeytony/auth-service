from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base


class UserSessionModel(Base):
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
    login_time: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now, nullable=False)
    logout_time: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    auth_user_id: Mapped[UUID] = mapped_column(ForeignKey('auth_user.auth_user_id', ondelete='CASCADE'), nullable=False)
    user_agent: Mapped[Optional[str]] = mapped_column(String(400), nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(15), nullable=False)
