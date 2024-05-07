from functools import lru_cache

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models import AuthUserModel

from .base_repository import BaseRepository


class AuthRepository(BaseRepository):
    """Репозиторий аутентификации и регистрации."""

    model = AuthUserModel

    async def register(self, user: dict) -> AuthUserModel:
        """Регистрация пользователя."""
        try:
            new_user = self.model(**user)
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Пользователь с таким email уже существует.',
            )
        return new_user

    async def login(self, user_email: str) -> AuthUserModel:
        """Вход пользователя в систему."""
        stmt = select(self.model).where(self.model.email == user_email)
        result = await self.session.execute(stmt)
        auth_user = result.scalar_one_or_none()
        if not auth_user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Пользователь не существует',
            )
        return auth_user


@lru_cache
def get_auth_repo(
    session: AsyncSession = Depends(get_session),
) -> AuthRepository:
    """Зависимость для репозитория аутентификации."""
    return AuthRepository(session)
