from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from repository import BaseRepository
from repository import get_role_repo
from schemas import RolesSchema
from schemas import SetUserRoleSchema
from schemas import UserRolesSchema

from .base_service import CrudService


class RoleService(
    CrudService,
):
    """Сервис для ролей."""

    schema = RolesSchema

    async def user_roles(self, user_id: UUID) -> UserRolesSchema:
        """Получение ролей пользователя."""
        user_roles = await self.repository.user_roles(user_id)
        return UserRolesSchema(roles=user_roles)

    # TODO: доразобраться с логикой добавления ролей
    async def set_user_role(self, user_role: SetUserRoleSchema) -> None:
        """Установка ролей пользователю."""
        await self.repository.set_user_role(user_role)


@lru_cache
def get_role_service(
    repository: BaseRepository = Depends(get_role_repo),
) -> RoleService:
    """Зависимость для сервиса ролей."""
    return RoleService(repository)
