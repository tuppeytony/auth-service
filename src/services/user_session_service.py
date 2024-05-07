from functools import lru_cache
from typing import Sequence
from uuid import UUID

from fastapi import Depends
from fastapi import Request

from repository import BaseRepository
from repository import get_user_session_repo
from schemas import UserSessionSchema
from utils import Paginator

from .base_service import BaseService


class UserSessionService(BaseService):
    """Сервис сессий пользователей."""

    schema = UserSessionSchema

    def __get_user_ip_addres(self, request: Request) -> str | None:
        return getattr(request.client, 'host', None)

    async def logging_start_session(self, user_id: UUID | str, user_agent: str | None, request: Request) -> None:
        """Запись входа пользователя в систему."""
        user_ip_address = self.__get_user_ip_addres(request)
        await self.repository.logging_start_session(user_id, user_agent, user_ip_address)

    async def logging_end_session(self, user_id: UUID | str) -> None:
        """Запись выхода пользователя из системы."""
        await self.repository.logging_end_session(user_id)

    # TODO: добавить функционал по сотритовке по полю
    async def users_activities(self, pagination: Paginator, ordering: Sequence[str]) -> list[UserSessionSchema]:
        """Просмотр активности пользователей."""
        users_activities = await self.repository.users_activities(pagination.limit, pagination.offset, ordering)
        return [self.schema.model_validate(user) for user in users_activities]

    async def user_activities(
        self,
        pagination: Paginator,
        ordering: Sequence[str],
        user_id: UUID,
    ) -> list[UserSessionSchema]:
        """Просмотр активности пользователя."""
        user_activities = await self.repository.user_activities(pagination.limit, pagination.offset, ordering, user_id)
        return [self.schema.model_validate(user) for user in user_activities]


@lru_cache
def get_user_session_service(
    repository: BaseRepository = Depends(get_user_session_repo),
) -> UserSessionService:
    """Получения сервиса сессий пользователя."""
    return UserSessionService(repository)
