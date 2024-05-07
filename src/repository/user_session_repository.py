from datetime import datetime
from functools import lru_cache
from typing import Any
from typing import Sequence
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models import AuthUserModel
from models import UserSessionModel

from .base_repository import BaseRepository


class UserSessionRepository(BaseRepository):
    """Репозиторий пользовательских сессий."""

    model = UserSessionModel

    async def logging_start_session(
        self,
        user_id: UUID | str,
        user_agent: str | None,
        user_ip_address: str | None,
    ) -> None:
        """Запись выхода пользователя из системы."""
        create_session = self.model(
            auth_user_id=user_id,
            ip_address=user_ip_address,
            user_agent=user_agent,
        )
        self.session.add(create_session)
        await self.session.commit()

    async def logging_end_session(self, user_id: UUID | str) -> None:
        """Запись выхода пользователя из системы."""
        stmt = select(self.model).where(
            self.model.auth_user_id == user_id,
        ).order_by(self.model.login_time.desc()).limit(1)
        result = await self.session.execute(stmt)
        user_session = result.scalar_one()
        user_session.logout_time = datetime.now()
        await self.session.commit()

    # TODO: добавить функционал по сотритовке по полю
    async def users_activities(self, limit: int, offset: int, ordering: Sequence[str]) -> Any:
        """Просмотр активности пользователей."""
        stmt = select(
            self.model.login_time,
            self.model.logout_time,
            self.model.user_agent,
            self.model.ip_address,
            AuthUserModel.creation_date,
            AuthUserModel.email,
            AuthUserModel.is_email_confirmed,
        ).join_from(
            self.model,
            AuthUserModel,
            self.model.auth_user_id == AuthUserModel.auth_user_id,
        ).order_by(
            *ordering,
        ).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.all()

    async def user_activities(
        self,
        limit: int,
        offset: int,
        ordering: Sequence[str],
        user_id: UUID,
    ) -> Any:
        """Просмотр активности пользователя."""
        stmt = select(
            self.model.login_time,
            self.model.logout_time,
            self.model.user_agent,
            self.model.ip_address,
            AuthUserModel.creation_date,
            AuthUserModel.email,
            AuthUserModel.is_email_confirmed,
        ).join_from(
            self.model,
            AuthUserModel,
            self.model.auth_user_id == AuthUserModel.auth_user_id,
        ).where(AuthUserModel.auth_user_id == user_id).order_by(
            *ordering,
        ).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.all()


@lru_cache
def get_user_session_repo(
    session: AsyncSession = Depends(get_session),
) -> UserSessionRepository:
    """Получение репозитория пользовательских сессий."""
    return UserSessionRepository(session)
