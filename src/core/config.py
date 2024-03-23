# mypy: disable-error-code="assignment"
import os

from datetime import timedelta
from functools import lru_cache

from async_fastapi_jwt_auth import AuthJWT
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


load_dotenv('./core/.env')


class AppSettings(BaseSettings):
    """Конфигурация приложения."""

    model_config = SettingsConfigDict(case_sensitive=False)

    api_prefix_url: str = '/api/v1'
    project_title: str = 'Сервис аутентификации и регистрации'
    docs_url: str = '/api/openapi'
    openapi_url: str = '/api/openapi.json'
    log_level: str = ...
    bases_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    debug: bool = False
    admin_email: str | None = Field(default=None, max_length=100)
    admin_password: str | None = None


class DataBaseSettings(BaseSettings):
    """Конфигурация подключения к БД."""

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix='DB_')

    host: str = ...
    port: int = ...
    user: str = ...
    password: str = ...
    name: str = ...
    driver: str = ...


class AuthJWTSettings(BaseSettings):
    """Конфигурация для токенов."""

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix='JWT_')

    authjwt_secret_key: str = ...
    authjwt_token_location: set[str]
    authjwt_access_token_expires: int = 15
    authjwt_refresh_token_expires: timedelta = timedelta(days=30)
    authjwt_cookie_csrf_protect: bool = True
    authjwt_cookie_secure: bool = ...


@AuthJWT.load_config
def get_auth_config() -> AuthJWTSettings:
    """Получение настроек для токенов."""
    return AuthJWTSettings()


@lru_cache
def get_db_settings() -> DataBaseSettings:
    """Получение настроек базы данных."""
    return DataBaseSettings()


@lru_cache
def get_app_settings() -> AppSettings:
    """Получение настроек приложения."""
    return AppSettings()


db_settings = get_db_settings()
app_settings = get_app_settings()
