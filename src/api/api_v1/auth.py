from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter
from fastapi import Depends

from core.config import app_settings
from schemas.user import UserLogin


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
    user: UserLogin,
    Authorize: AuthJWT = Depends(),
) -> None:
    """Регистрация пользователя."""
    ...


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
