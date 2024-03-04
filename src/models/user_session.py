from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from .base import Base


class UserSessionModel(Base):
    """Модель сессий пользователя."""

    __tablename__ = 'user_session'

    def __init__(
        self,
        auth_user_id: UUID,
        logout_time: datetime | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ):
        self.auth_user_id = auth_user_id
        self.logout_time = logout_time
        self.user_agent = user_agent
        self.ip_address = ip_address

    session_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    login_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, server_default=func.now())
    logout_time: Mapped[datetime | None] = mapped_column(DateTime)
    auth_user_id: Mapped[UUID] = mapped_column(ForeignKey('auth_user.auth_user_id', ondelete='CASCADE'))
    user_agent: Mapped[str | None] = mapped_column(String(400))
    ip_address: Mapped[str | None] = mapped_column(String(15))
