from datetime import datetime
from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from fastapi import Request
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

    def __get_user_ip_addres(self, request: Request) -> str | None:
        return getattr(request.client, 'host', None)

    async def logging_start_session(self, user_id: UUID | str, user_agent: str | None, request: Request) -> None:
        """Запись входа пользователя в систему."""
        user_ip_address = self.__get_user_ip_addres(request)
        create_session = UserSession(
            auth_user_id=user_id,
            ip_address=user_ip_address,
            user_agent=user_agent,
        )
        self.session.add(create_session)
        await self.session.commit()

    async def logging_end_session(self, user_id: UUID | str) -> None:
        """Запись выхода пользователя из системы."""
        stmt = select(UserSession).where(
            UserSession.auth_user_id == user_id,
        ).order_by(UserSession.login_time.desc()).limit(1)
        result = await self.session.execute(stmt)
        user_session = result.scalar_one()
        user_session.logout_time = datetime.now()
        await self.session.commit()

    # TODO: добавить функционал по сотритовке по полю
    async def users_activities(self, pagination: Paginator, ordering: str) -> list[UserSessionSchema]:  # noqa: U100
        """Просмотр активности пользователей."""
        stmt = select(
            UserSession.login_time,
            UserSession.logout_time,
            UserSession.user_agent,
            UserSession.ip_address,
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
