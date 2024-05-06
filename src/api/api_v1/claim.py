from typing import Annotated
from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path

from core.config import app_settings
from schemas import ClaimSchema
from schemas import CreateClaimSchema
from schemas import UpdateClaimSchema
from services import ClaimService
from services import get_auth_jwt_bearer
from services import get_claim_service


router = APIRouter(prefix=app_settings.api_prefix_url, tags=['Добавление данных в токен'])


@router.get(
    '/user-claim/{user_id}',
    description='Просмотр user claims для пользователя',
    summary='Просмотр user claims для пользователя',
    response_model=list[ClaimSchema],
)
async def retrive_user_claims(
    user_id: Annotated[UUID, Path(description='id пользователя')],
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
    claim_service: ClaimService = Depends(get_claim_service),
) -> list[ClaimSchema]:
    """Получение свойтв пользователя."""
    await Authorize.jwt_required()
    user_claims = await claim_service.get_user_claims(user_id)
    return user_claims


@router.post(
    '/user-claim',
    description='Добавлениние пользователю claim',
    summary='Добавлениние пользователю claim',
    response_model=ClaimSchema,
)
async def add_to_user_claim(
    new_claim: CreateClaimSchema,
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
    claim_service: ClaimService = Depends(get_claim_service),
) -> ClaimSchema:
    """Добавление свойства для пользователя."""
    await Authorize.jwt_required()
    new_claim = await claim_service.create_claim(new_claim)
    return new_claim


@router.patch(
    '/user-claim/{user_id}',
    description='изменение пользователю claims',
    summary='изменение пользователю claims',
    response_model=UpdateClaimSchema,
)
async def update_user_claims(
    user_id: Annotated[UUID, Path(description='id пользователя')],
    updated_claim: UpdateClaimSchema,
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
    claim_service: ClaimService = Depends(get_claim_service),
) -> UpdateClaimSchema:
    """Обновление свойства пользователя."""
    await Authorize.jwt_required()
    updated_user_claim = await claim_service.update_user_claim(user_id, updated_claim)
    return updated_user_claim


@router.delete(
    '/user-claim/{user_id}',
    description='Удаление у пользователя claims',
    summary='Удаление у пользователя claims',
)
async def delete_user_claims(
    user_id: Annotated[UUID, Path(description='id пользователя')],
    claim_id: UUID,
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
    claim_service: ClaimService = Depends(get_claim_service),
) -> dict[str, str]:
    """Удаление свойства пользователя."""
    await Authorize.jwt_required()
    await claim_service.delete_user_claim(user_id, claim_id)
    return {'status': 'ok'}
