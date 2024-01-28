from functools import lru_cache

from fastapi import Depends
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
        new_user = AuthUser(**user.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return str(new_user.auth_user_id)


@lru_cache
def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    """Получение сервиса аутентификаций."""
    return AuthService(session)
