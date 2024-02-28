from typing import AsyncGenerator
from typing import Optional

import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from src.db.postgres import get_session
from src.main import app
from src.models import AuthUser
from src.models import Base
from tests.functional.settings import tests_settings
from tests.functional.testdata.database_mapping import database_data


async_session: Optional[AsyncSession] = None
dsn = (
    f'{tests_settings.db_driver}://{tests_settings.db_user}:{tests_settings.db_password}'
    f'@{tests_settings.db_host}:{tests_settings.db_port}/{tests_settings.db_name}'
)
engine_test = create_async_engine(dsn, echo=True, future=True)


async def override_get_session() -> AsyncSession:  # type: ignore
    """Получение сессия для тестирования."""
    async with async_session() as session:  # type: ignore
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture(autouse=True, scope='session')
async def _prepare_db() -> AsyncGenerator:
    """Подготовка БД для тестов."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine_test) as session:
        async with session.begin():
            session.add_all([AuthUser(**user) for user in database_data])
        await session.commit()
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
