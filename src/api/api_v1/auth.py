from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter
from fastapi import Depends

from core.config import app_settings
from schemas.token import TokenSchema
from schemas.user import UserLogin
from schemas.user import UserRegister
from schemas.user import UserRestorePassword
from services.auth_service import AuthService
from services.auth_service import get_auth_service
from services.user_session_service import UserSessionService
from services.user_session_service import get_user_session_service


router = APIRouter(tags=['Аутентификация и регистрация'], prefix=app_settings.api_prefix_url)


@router.post(
    '/login',
    description='Аутентификация',
    summary='Аутентификация',
    response_model=TokenSchema,
)
async def login(
    user: UserLogin,
    Authorize: AuthJWT = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
    user_session_service: UserSessionService = Depends(get_user_session_service),
) -> TokenSchema:
    """Аутентифицация пользователя."""
    user_id = await auth_service.login(user)
    await user_session_service.set_login_time(user_id)
    refresh_token = await Authorize.create_refresh_token(subject=user_id)
    access_token = await Authorize.create_access_token(subject=user_id)
    await Authorize.set_access_cookies(access_token)
    await Authorize.set_refresh_cookies(refresh_token)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post(
    '/registration',
    description='Регистрация',
    summary='Регистрация пользователя',
    response_model=TokenSchema,
)
async def registration(
    user: UserRegister,
    Authorize: AuthJWT = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
    user_session_service: UserSessionService = Depends(get_user_session_service),
) -> TokenSchema:
    """Регистрация пользователя."""
    user_id = await auth_service.register(user)
    await user_session_service.set_login_time(user_id)
    refresh_token = await Authorize.create_refresh_token(subject=user_id)
    access_token = await Authorize.create_access_token(subject=user_id)
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
    Authorize: AuthJWT = Depends(),
) -> TokenSchema:
    """Обновление токена."""
    await Authorize.jwt_refresh_token_required()
    current_user = await Authorize.get_jwt_subject()
    new_access_token = await Authorize.create_access_token(subject=current_user)
    new_refresh_token = await Authorize.create_refresh_token(subject=current_user)
    await Authorize.set_access_cookies(new_access_token)
    return TokenSchema(access_token=new_access_token, refresh_token=new_refresh_token)


@router.delete(
    '/logout',
    description='Выход из приложения',
    summary='Выход из приложения',
)
async def logout(
    Authorize: AuthJWT = Depends(),
    user_session_service: UserSessionService = Depends(get_user_session_service),
) -> None:
    """Логаут пользователя."""
    await Authorize.jwt_required()
    user_id = await Authorize.get_jwt_subject()
    await user_session_service.set_logout_time(user_id)
    await Authorize.unset_jwt_cookies()


@router.post(
    '/restore-password',
    description='Восстановление пароля',
    summary='Восстановление пароля',
)
async def restore_password(
    user_email: UserRestorePassword,
) -> None:
    """Восстановление пароля."""
    ...
