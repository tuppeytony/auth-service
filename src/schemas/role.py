from uuid import UUID

from .base_schema import BaseSchema


class RolesSchema(BaseSchema):
    """Схема для ролей."""

    role_id: UUID
    role_name: str


class CreateRoleSchema(BaseSchema):
    """Схема для создания ролей."""

    role_name: str


class UpdateRoleSchema(CreateRoleSchema):
    """Схема для обновления ролей."""

    pass


class SetUserRoleSchema(BaseSchema):
    """Схема для установки ролей пользователю."""

    user_id: UUID
    role_id: list[UUID]
