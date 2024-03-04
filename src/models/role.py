from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


if TYPE_CHECKING:
    from .auth_user import AuthUserModel


class RoleModel(Base):
    """Модель для ролей."""

    __tablename__ = 'role'

    role_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    role_name: Mapped[str] = mapped_column(String(100), unique=True)
    # при связях M2M и использовании другой схемы, нужно ее явно прописывать в secondary
    user: Mapped['AuthUserModel'] = relationship(
        secondary='auth_service.role_auth_user_association',
        back_populates='roles',
    )
