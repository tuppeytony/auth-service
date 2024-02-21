from datetime import datetime
from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models.auth_user_entity import AuthUser
from models.auth_user_entity import UserSession
from schemas.user_session import UserSessionSchema
from utils.pagination import Paginator


class UserSessionService:
    """Сервис сессий пользователей."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def set_login_time(self, user_id: UUID | str) -> None:
        """Запись время входа пользователя в систему."""
        create_session = UserSession(user_id)
        self.session.add(create_session)
        await self.session.commit()

    async def set_logout_time(self, user_id: UUID | str) -> None:
        """Запись времени выхода пользователя из системы."""
        stmt = select(UserSession).where(
            UserSession.auth_user_id == user_id,
        ).order_by(UserSession.login_time.desc()).limit(1)
        result = await self.session.execute(stmt)
        user_session = result.scalar_one()
        user_session.logout_time = datetime.now()
        await self.session.commit()

    async def users_activities(self, pagination: Paginator, ordering: str) -> list[UserSessionSchema]:
        """Просмотр активности пользователей."""
        stmt = select(
            UserSession.login_time,
            UserSession.logout_time,
            AuthUser.creation_date,
            AuthUser.email,
            AuthUser.is_email_confirmed,
        ).join_from(
            UserSession,
            AuthUser,
            UserSession.auth_user_id == AuthUser.auth_user_id,
        ).order_by(
            AuthUser.email,
        ).limit(pagination.limit).offset(pagination.offset)
        result = await self.session.execute(stmt)
        return [UserSessionSchema.model_validate(user) for user in result.all()]


@lru_cache
def get_user_session_service(session: AsyncSession = Depends(get_session)) -> UserSessionService:
    """Получения сервиса сессий пользователя."""
    return UserSessionService(session)
