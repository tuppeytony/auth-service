from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter
from fastapi import Depends

from core.config import app_settings
from schemas.user import UserLogin
from schemas.user import UserRegister
from schemas.user import UserRestorePassword
from services.auth_service import AuthService
from services.auth_service import get_auth_service


router = APIRouter(tags=['Аутентификация и регистрация'], prefix=f'{app_settings.api_prefix_url}')


@router.post(
    '/login',
    description='Аутентификация',
    summary='Аутентификация',
)
async def login(
    user: UserLogin,
    Authorize: AuthJWT = Depends(),
) -> None:
    """Аутентифицация пользователя."""
    ...


@router.post(
    '/registration',
    description='Регистрация',
    summary='Регистрация пользователя',
)
async def registration(
    user: UserRegister,
    Authorize: AuthJWT = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    """Регистрация пользователя."""
    user_id = await auth_service.register(user)
    refresh_token = await Authorize.create_refresh_token(subject=user_id)
    access_token = await Authorize.create_access_token(subject=user_id)
    await Authorize.set_access_cookies(access_token)
    await Authorize.set_refresh_cookies(refresh_token)
    return {'result': user_id}


@router.post(
    '/refresh',
    description='Обновление токенов',
    summary='Обновление токенов',
)
async def refresh_token(
    Authorize: AuthJWT = Depends(),
) -> None:
    """Обновление токена."""
    ...


@router.delete(
    '/logout',
    description='Выход из приложения',
    summary='Выход из приложения',
)
async def logout(
    Authorize: AuthJWT = Depends(),
) -> None:
    """Логаут пользователя."""
    ...


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
