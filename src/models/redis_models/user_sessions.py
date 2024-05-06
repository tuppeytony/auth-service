from datetime import datetime
from uuid import UUID
from uuid import uuid4

from aredis_om import Field

from .base_redis_model import BaseRedisHashModel


class UserSessionModel(BaseRedisHashModel):
    """Таблица для сессий пользователя."""

    user_id: UUID = Field(index=True)
    refresh_token_id: UUID = Field(default_factory=lambda: uuid4(), index=True)
    refresh_token: str
    user_agent: str = Field(max_length=200, index=True)
    ip_address: str = Field(max_length=15, index=True)
    expires_in: int
    created_at: datetime = Field(default_factory=lambda: datetime.now())
