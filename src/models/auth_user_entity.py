from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class AuthUser(Base):
    """Таблица аутентификационного пользователя."""

    __tablename__ = 'auth_user'

    def __init__(self, email, password):
        self.email = email
        self.password = password

    auth_user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
