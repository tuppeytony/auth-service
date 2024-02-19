from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from core.config import app_settings
from core.config import db_settings


async_session: Optional[AsyncSession] = None
dsn = (
    f'{db_settings.driver}://{db_settings.user}:{db_settings.password}'
    f'@{db_settings.host}:{db_settings.port}/{db_settings.name}'
)
engine = create_async_engine(dsn, echo=app_settings.debug, future=True)


async def get_session() -> AsyncSession:  # type: ignore
    """Получение сессия для работы с базой данных."""
    async with async_session() as session:  # type: ignore
        yield session
