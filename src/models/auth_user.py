from datetime import date
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .base import Base


if TYPE_CHECKING:
    from .role import RoleModel


class AuthUserModel(Base):
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
    roles: Mapped[list['RoleModel']] = relationship(
        secondary='role',
        back_populates='role_id',
    )

    def check_user_hash_password(self, password: str) -> bool:
        """Проверка хэша пароля пользователя."""
        return check_password_hash(self.password, password)
