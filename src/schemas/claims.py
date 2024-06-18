from uuid import UUID

from pydantic import Field

from .base_schema import BaseSchema


class ClaimSchema(BaseSchema):
    """Схема для свойств пользователя."""

    claim_name: str = Field(max_length=15)
    claim_value: str = Field(max_length=25)


class CreateClaimSchema(ClaimSchema):
    """Схема для создания свойства пользоаетлю."""

    user_id: UUID


class UpdateClaimSchema(ClaimSchema):
    """Схема для обновления свойства пользователя."""

    pass
