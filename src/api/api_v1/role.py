from typing import Annotated
from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path

from core.config import app_settings
from schemas import CreateRoleSchema
from schemas import RolesSchema
from schemas import SetUserRoleSchema
from schemas import UpdateRoleSchema
from schemas import UserRolesSchema
from services import RoleService
from services import get_auth_jwt_bearer
from services import get_role_service
from utils import Paginator


router = APIRouter(prefix=app_settings.api_prefix_url, tags=['Роли'])


@router.get(
    '/roles',
    description='Список всех ролей',
    summary='Список всех ролей',
    response_model=list[RolesSchema],
)
async def roles(
    role_service: RoleService = Depends(get_role_service),
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
    pagination: Paginator = Depends(Paginator),
) -> list[RolesSchema]:
    """Получе ролей."""
    await Authorize.jwt_required()
    roles = await role_service.get_all(pagination, ('role_name', ))
    return roles


@router.get(
    '/roles/{role_id}',
    description='Просмотр роли',
    summary='Просмотр роли',
    response_model=RolesSchema,
)
async def retrive_role(
    role_id: Annotated[UUID, Path(description='id роли')],
    role_service: RoleService = Depends(get_role_service),
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
) -> RolesSchema:
    """Получение роли."""
    await Authorize.jwt_required()
    role = await role_service.get_one(role_id)
    return role


@router.post(
    '/roles',
    description='Создание роли',
    summary='Создание роли',
    response_model=RolesSchema,
)
async def create_role(
    role: CreateRoleSchema,
    role_service: RoleService = Depends(get_role_service),
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
) -> RolesSchema:
    """Создание роли."""
    await Authorize.jwt_required()
    new_role = await role_service.create(role)
    return new_role


@router.delete(
    '/roles/{role_id}',
    description='Удаление роли',
    summary='Удаление роли',
)
async def delete_role(
    role_id: Annotated[UUID, Path(description='id пользователя')],
    role_service: RoleService = Depends(get_role_service),
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
) -> dict:
    """Удаление роли."""
    await Authorize.fresh_jwt_required()
    await role_service.delete(role_id)
    return {'status': 'ok'}


@router.patch(
    '/roles/{role_id}',
    description='изменение роли',
    summary='изменение роли',
    response_model=RolesSchema,
)
async def update_role(
    role_id: Annotated[UUID, Path(description='id роли')],
    role: UpdateRoleSchema,
    role_service: RoleService = Depends(get_role_service),
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
) -> RolesSchema:
    """изменение роли."""
    await Authorize.jwt_required()
    updated_role = await role_service.update(role_id, role)
    return updated_role


@router.post(
    '/set-role',
    description='Добавление пользоватею роли',
    summary='Добавление пользоватею роли',
)
async def set_user_role(
    user_role: SetUserRoleSchema,
    role_service: RoleService = Depends(get_role_service),
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
) -> dict:
    """Добавление роли пользователю."""
    await Authorize.fresh_jwt_required()
    await role_service.set_user_role(user_role)
    return {'status': 'ok'}


@router.get(
    '/user-roles/{user_id}',
    description='Просмотр назначенных ролей пользователю',
    summary='Просмотр назначенных ролей пользователю',
    response_model=UserRolesSchema,
)
async def user_roles(
    user_id: Annotated[UUID, Path(description='id пользователя')],
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
    role_service: RoleService = Depends(get_role_service),
) -> UserRolesSchema:
    """Получение ролей пользователя."""
    Authorize.jwt_required()
    user_roles = await role_service.user_roles(user_id)
    return user_roles
