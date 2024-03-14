from uuid import UUID

from .base_schema import BaseSchema


class ClaimSchema(BaseSchema):
    """Схема для свойств пользователя."""

    claim_name: str
    claim_value: str


class CreateClaimSchema(ClaimSchema):
    """Схема для создания свойства пользоаетлю."""

    user_id: UUID


class UpdateClaimSchema(ClaimSchema):
    """Схема для обновления свойства пользователя."""

    pass
