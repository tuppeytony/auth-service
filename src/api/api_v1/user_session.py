from typing import Annotated
from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from core.config import app_settings
from schemas import UserSessionSchema
from services.user_session_service import UserSessionService
from services.user_session_service import get_user_session_service
from utils.pagination import Paginator


router = APIRouter(tags=['Сессии пользователей'], prefix=app_settings.api_prefix_url)


@router.get(
    '/users',
    description='Список активностей пользователей',
    summary='Список активностей пользователей',
    response_model=list[UserSessionSchema],
)
async def users_activities(
    user_session_service: UserSessionService = Depends(get_user_session_service),
    Authorize: AuthJWT = Depends(),
    pagination: Paginator = Depends(Paginator),
    ordering: Annotated[str, Query(description='Сортировка пользователей')] = 'email',
) -> list[UserSessionSchema]:
    """Список активностей пользователей."""
    await Authorize.jwt_required()
    users_activities = await user_session_service.users_activities(pagination, ordering)
    return users_activities


@router.get(
    '/user/{user_id}',
    description='Активность пользователя',
    summary='Активность пользователя',
    response_model=list[UserSessionSchema],
)
async def user_activities(
    user_id: UUID,
    Authorize: AuthJWT = Depends(),
    user_session_service: UserSessionService = Depends(get_user_session_service),
    pagination: Paginator = Depends(Paginator),
    ordering: Annotated[str, Query(description='Сортировка пользователей')] = 'email',
) -> list[UserSessionSchema]:
    """Активность пользователя."""
    await Authorize.jwt_required()
    user_activities = await user_session_service.user_activities(pagination, ordering, user_id)
    return user_activities
