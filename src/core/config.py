# mypy: disable-error-code="assignment"
import os

from functools import lru_cache

from async_fastapi_jwt_auth import AuthJWT
from dotenv import load_dotenv
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
    debug: bool = True


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

    authjwt_secret_key: str
    authjwt_token_location: set[str]


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
