# mypy: disable-error-code="assignment"
import os

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

    authjwt_refresh_cookie_key: str = 'refresh_token_cookie'
    authjwt_refresh_token_expires: int = 86400 * 30


class DataBaseSettings(BaseSettings):
    """Конфигурация подключения к БД."""

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix='DB_')

    host: str = ...
    port: int = ...
    user: str = ...
    password: str = ...
    name: str = ...
    driver: str = ...


class CacheSettings(BaseSettings):
    """Настройки для кэша."""

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix='CACHE_')

    host: str = ...
    port: int = ...
    user: str | None = None
    password: str | None = None
    decode_responses: bool = True


class AuthJWTSettings(BaseSettings):
    """Конфигурация для токенов."""

    model_config = SettingsConfigDict(case_sensitive=False)

    authjwt_secret_key: str = ...
    authjwt_token_location: set[str]
    authjwt_access_token_expires: int = 15
    # 30 дней
    authjwt_refresh_token_expires: int = 86400 * 30
    authjwt_cookie_csrf_protect: bool = True
    authjwt_cookie_secure: bool = ...
    authjwt_access_cookie_key: str = 'access_token_cookie'
    authjwt_refresh_cookie_key: str = 'refresh_token_cookie'


@AuthJWT.load_config
def get_auth_config() -> AuthJWTSettings:
    """Получение настроек для токенов."""
    return AuthJWTSettings()


db_settings = DataBaseSettings()
cache_settings = CacheSettings()
app_settings = AppSettings()
