from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base


class ClaimModel(Base):
    """Модель свойств."""

    __tablename__ = 'claim'
    __table_args__ = (
        UniqueConstraint('claim_name', 'user_id', name='idx_unique_user_id_claim_name'),
    )
    pk = 'claim_id'

    def __init__(
        self,
        claim_name: str,
        claim_value: str,
        user_id: UUID,
    ) -> None:
        self.claim_name = claim_name.lower()
        self.claim_value = claim_value
        self.user_id = user_id

    claim_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=text('gen_random_uuid()'),
    )
    claim_name: Mapped[str] = mapped_column(String(length=15))
    claim_value: Mapped[str] = mapped_column(String(length=25))
    user_id: Mapped[UUID] = mapped_column(ForeignKey('auth_user.auth_user_id', ondelete='CASCADE'))
