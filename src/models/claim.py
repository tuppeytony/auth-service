from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base


class ClaimModel(Base):
    """Модель свойств."""

    __tablename__ = 'claim'
    pk = 'claim_id'

    claim_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=text('gen_random_uuid()'),
    )
    claim_name: Mapped[str] = mapped_column(String(length=15))
    claim_value: Mapped[str] = mapped_column(String(length=25))
    user_id: Mapped[UUID] = mapped_column(ForeignKey('auth_user.auth_user_id', ondelete='CASCADE'))
