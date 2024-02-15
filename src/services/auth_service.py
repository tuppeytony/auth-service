from functools import lru_cache

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models.auth_user_entity import AuthUser
from schemas.user import UserRegister


class AuthService:
    """Сервис аутентификаций."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def register(self, user: UserRegister) -> str:
        """Регистрация пользователя."""
        try:
            new_user = AuthUser(**user.model_dump())
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Пользователь с таким email уже существует.',
            )
        return str(new_user.auth_user_id)

    async def login(self, user: UserRegister) -> str:
        """Вход пользователя в систему."""
        stmt = select(AuthUser).where(AuthUser.email == user.email)
        result = await self.session.execute(stmt)
        auth_user = result.scalar_one_or_none()
        if not auth_user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Пользователь не существует',
            )
        self.__validate_user(auth_user, user)
        return str(auth_user.auth_user_id)

    def __validate_user(self, auth_user: AuthUser, user: UserRegister) -> None:
        """Проверка пользователя при входе."""
        if not auth_user.check_user_hash_password(user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Не правильный пароль',
            )


@lru_cache
def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    """Получение сервиса аутентификаций."""
    return AuthService(session)
