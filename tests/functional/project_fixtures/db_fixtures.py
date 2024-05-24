from pathlib import Path
from typing import Any
from typing import AsyncGenerator
from typing import Optional

import docker
import docker.errors
import pytest
import pytest_asyncio

from docker.models.containers import Container
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from src.db.postgres import get_session
from src.main import app
from src.models import AuthUserModel
from src.models import Base
from tests.functional.settings import tests_settings
from tests.functional.testdata.database_mapping import database_data
from tests.functional.utils.utils import wait_until_docker_healthy


async_session: Optional[AsyncSession] = None


async def override_get_session() -> AsyncSession:  # type: ignore
    """Получение сессия для тестирования."""
    async with async_session() as session:  # type: ignore
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope='session')
def create_db() -> Any:
    """Создания докер контейнера для тестовой базы."""
    client = docker.from_env()
    path_to_schema = Path.cwd() / 'db_schema.sql'
    postgres = client.containers.run(
        'postgres:13',
        environment={
            'POSTGRES_PASSWORD': tests_settings.db_password,
            'POSTGRES_USER': tests_settings.db_user,
            'POSTGRES_DB': tests_settings.db_name,
        },
        volumes=[f'{path_to_schema.absolute()}:/docker-entrypoint-initdb.d/db_schema.sql'],
        ports={
            '5432/tcp': int(tests_settings.db_port),
        },
        healthcheck={
            'test': ['CMD-SHELL', f"sh -c 'pg_isready -U {tests_settings.db_user} -d {tests_settings.db_name}'"],
            'interval': 10 * 1_000_000_000,
            'timeout': 10 * 1_000_000_000,
            'retries': 5,
        },
        detach=True,
    )
    wait_until_docker_healthy(postgres, client)
    return postgres


@pytest.fixture(scope='session')
def db_engine() -> AsyncEngine:
    """Создания движка для ОРМ."""
    dsn = (
        f'{tests_settings.db_driver}://{tests_settings.db_user}:{tests_settings.db_password}'
        f'@{tests_settings.db_host}:{tests_settings.db_port}/{tests_settings.db_name}'
    )
    return create_async_engine(dsn, echo=True, future=True)


@pytest_asyncio.fixture(autouse=True, scope='session')
async def _prepare_db(create_db: Container, db_engine: AsyncEngine) -> AsyncGenerator:
    """Подготовка БД для тестов."""
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(db_engine) as session:
        async with session.begin():
            session.add_all([AuthUserModel(**user) for user in database_data])  # type: ignore[arg-type]
        await session.commit()
    yield
    create_db.stop()
    create_db.remove()
