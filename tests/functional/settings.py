# mypy: disable-error-code="assignment"
from dotenv import load_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


load_dotenv('./tests/functional/.env')


class FunctioalTestSettings(BaseSettings):
    """Настройки для функциональных тестов."""

    model_config = SettingsConfigDict(case_sensitive=False)

    service_url: str = ...
    api_version: str = ...
    db_driver: str = ...
    db_user: str = ...
    db_password: str = ...
    db_host: str = ...
    db_port: str = ...
    db_name: str = ...

    @computed_field  # type: ignore[misc]
    @property
    def service_api_url(self) -> str:
        """URL сервиса."""
        return f'{self.service_url}/api/{self.api_version}'


tests_settings = FunctioalTestSettings()
