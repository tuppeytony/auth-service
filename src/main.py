from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn

from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from api.api_v1 import auth
from core.config import app_settings
from db import postgres


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Подключение к БД."""
    postgres.async_session = sessionmaker(
        postgres.engine, class_=AsyncSession, expire_on_commit=False,
    )
    yield


app = FastAPI(
    title=app_settings.project_title,
    docs_url=app_settings.docs_url,
    openapi_url=app_settings.openapi_url,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> ORJSONResponse:
    """Хэндлер для обработки исключений токенов."""
    return ORJSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message},
    )


app.include_router(auth.router)

if __name__ == '__main__':
    uvicorn.run(app)
