from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

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

if __name__ == '__main__':
    uvicorn.run(app)
