from typing import Annotated

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import Request
from fastapi import status

from core.config import app_settings
from schemas import TokenSchema
from schemas import UserLoginSchema
from schemas import UserRegisterSchema
from schemas import UserRestorePasswordSchema
from services import AuthService
from services import RoleService
from services import UserSessionService
from services import get_auth_jwt_bearer
from services import get_auth_service
from services import get_role_service
from services import get_user_session_service


router = APIRouter(tags=['Аутентификация и регистрация'], prefix=app_settings.api_prefix_url)


@router.post(
    '/login',
    description='Аутентификация',
    summary='Аутентификация',
    response_model=TokenSchema,
)
async def login(
    user: UserLoginSchema,
    request: Request,
    user_agent: Annotated[str | None, Header(
        examples=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/122.0.0.0 Safari/537.36'],
    )] = None,
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
    auth_service: AuthService = Depends(get_auth_service),
    user_session_service: UserSessionService = Depends(get_user_session_service),
    role_service: RoleService = Depends(get_role_service),
) -> TokenSchema:
    """Аутентифицация пользователя."""
    user_id = await auth_service.login(user)
    await user_session_service.logging_start_session(user_id, user_agent, request)
    user_roles = await role_service.user_roles(user_id)
    refresh_token = await Authorize.create_refresh_token(subject=user_id)
    # TODO: добавить эндпоинт, что бы можно было добавлять разные еще usert_claims
    access_token = await Authorize.create_access_token(
        subject=user_id,
        user_claims=user_roles.model_dump(),
    )
    await Authorize.set_access_cookies(access_token)
    await Authorize.set_refresh_cookies(refresh_token)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post(
    '/registration',
    description='Регистрация',
    summary='Регистрация пользователя',
    response_model=TokenSchema,
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    user: UserRegisterSchema,
    request: Request,
    user_agent: Annotated[str | None, Header(
        examples=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/122.0.0.0 Safari/537.36'],
    )] = None,
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
    auth_service: AuthService = Depends(get_auth_service),
    user_session_service: UserSessionService = Depends(get_user_session_service),
    role_service: RoleService = Depends(get_role_service),
) -> TokenSchema:
    """Регистрация пользователя."""
    user_id = await auth_service.register(user)
    await user_session_service.logging_start_session(user_id, user_agent, request)
    refresh_token = await Authorize.create_refresh_token(subject=user_id)
    user_roles = await role_service.user_roles(user_id)
    access_token = await Authorize.create_access_token(
        subject=user_id,
        user_claims=user_roles.model_dump(),
    )
    await Authorize.set_access_cookies(access_token)
    await Authorize.set_refresh_cookies(refresh_token)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post(
    '/refresh',
    description='Обновление токенов',
    summary='Обновление токенов',
    response_model=TokenSchema,
)
async def refresh_token(
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
    role_service: RoleService = Depends(get_role_service),
) -> TokenSchema:
    """Обновление токена."""
    await Authorize.jwt_refresh_token_required()
    current_user = await Authorize.get_jwt_subject()
    user_roles = await role_service.user_roles(current_user)
    new_access_token = await Authorize.create_access_token(
        subject=current_user,
        user_claims=user_roles.model_dump(),
    )
    new_refresh_token = await Authorize.create_refresh_token(subject=current_user)
    await Authorize.set_access_cookies(new_access_token)
    return TokenSchema(access_token=new_access_token, refresh_token=new_refresh_token)


@router.delete(
    '/logout',
    description='Выход из приложения',
    summary='Выход из приложения',
)
async def logout(
    Authorize: AuthJWT = Depends(get_auth_jwt_bearer),
    user_session_service: UserSessionService = Depends(get_user_session_service),
) -> dict:
    """Логаут пользователя."""
    await Authorize.jwt_required()
    user_id = await Authorize.get_jwt_subject()
    await user_session_service.logging_end_session(user_id)
    await Authorize.unset_jwt_cookies()
    return {'status': 'ok'}


@router.post(
    '/restore-password',
    description='Восстановление пароля',
    summary='Восстановление пароля',
)
async def restore_password(
    user_email: UserRestorePasswordSchema,  # noqa: U100
) -> None:
    """Восстановление пароля."""
    ...
