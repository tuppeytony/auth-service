# mypy: disable-error-code="assignment"
import os

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

    authjwt_secret_key: str = 'secret'
    authjwt_token_location: set = {'cookies'}


@AuthJWT.load_config
def get_auth_config() -> AuthJWTSettings:
    """Получение настроек для токенов."""
    return AuthJWTSettings()


db_settings = DataBaseSettings()
app_settings = AppSettings()
