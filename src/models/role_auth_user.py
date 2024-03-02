from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base


class RoleAuthUserAssociation(Base):
    """Модель для M2M пользователя и роли."""

    __tablename__ = 'role_auth_user_association'
    __table_args__ = (
        UniqueConstraint('auth_user_id', 'role_id', name='idx_unique_auth_user_id_role_id'),
    )

    role_auth_user_association_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    auth_user_id: Mapped[UUID] = mapped_column(ForeignKey('auth_user.auth_user_id'))
    role_id: Mapped[UUID] = mapped_column(ForeignKey('role.role_id'))
