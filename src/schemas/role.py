from uuid import UUID

from pydantic import Field

from .base_schema import BaseSchema


class RolesSchema(BaseSchema):
    """Схема для ролей."""

    role_id: UUID
    role_name: str


class CreateRoleSchema(BaseSchema):
    """Схема для создания ролей."""

    role_name: str = Field(max_length=100)


class UpdateRoleSchema(CreateRoleSchema):
    """Схема для обновления ролей."""

    pass


class SetUserRoleSchema(BaseSchema):
    """Схема для установки ролей пользователю."""

    user_id: UUID
    roles_id: set[UUID]


class UserRolesSchema(BaseSchema):
    """Схема для ролей пользователя."""

    roles: list[str] | None
