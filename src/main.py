from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn

from aredis_om import Migrator
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from api import healthcheck
from api.api_v1 import auth
from api.api_v1 import claim
from api.api_v1 import role
from api.api_v1 import user_session
from core.config import app_settings
from core.config import cache_settings
from db import postgres
from db import redis
from utils import CreateAdmin


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:  # noqa: U100
    """Подключение к БД."""
    postgres.async_session = sessionmaker(
        postgres.engine, class_=AsyncSession, expire_on_commit=False,
    )
    redis.redis = Redis(**cache_settings.model_dump(exclude_none=True))
    await Migrator().run()
    await CreateAdmin(postgres.async_session).create_admin()
    yield


app = FastAPI(
    title=app_settings.project_title,
    docs_url=app_settings.docs_url,
    openapi_url=app_settings.openapi_url,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    debug=app_settings.debug,
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> ORJSONResponse:  # noqa: U100
    """Хэндлер для обработки исключений токенов."""
    return ORJSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message},
    )


app.include_router(auth.router)
app.include_router(user_session.router)
app.include_router(role.router)
app.include_router(claim.router)

app.include_router(healthcheck.router)

if __name__ == '__main__':
    uvicorn.run(app)
