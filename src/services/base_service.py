# mypy: disable-error-code="attr-defined"
from abc import ABC
from abc import abstractmethod
from typing import Sequence

from repository import BaseRepository
from schemas.base_schema import BaseSchema
from utils import Paginator
from utils.consts import PrimaryKey


class BaseService:
    """интерфейс для сервисов."""

    schema: BaseSchema = None
    pagination: Paginator = None

    def __init__(self, repository: BaseRepository):
        self.repository = repository


class BaseCreateService(ABC):
    """Базовый класс для сервиса создания."""

    @abstractmethod
    async def create(self, creation_data: BaseSchema) -> BaseSchema:  # noqa: U100
        """Создание."""
        ...


class BaseUpdateService(ABC):
    """Базовый серис обновления."""

    @abstractmethod
    async def update(self, pk: PrimaryKey, update_data: BaseSchema) -> BaseSchema:  # noqa: U100
        """Обновление."""
        ...


class BaseDeleteService(ABC):
    """Базовый класс для удаления."""

    @abstractmethod
    async def delete(self, pk: PrimaryKey) -> None:  # noqa: U100
        """Удаление."""
        ...


class BaseRetriveService(ABC):
    """Базовый класс для получения по первичному ключу."""

    @abstractmethod
    async def get_one(self, pk: PrimaryKey) -> BaseSchema:  # noqa: U100
        """Получение по первичному ключу."""
        ...


class BaseListService(ABC):
    """Базовый класс для получения списка элеметнов."""

    @abstractmethod
    async def get_all(self, pagination: Paginator, ordering: Sequence[str]) -> list[BaseSchema]:  # noqa: U100
        """Получение списка элементов."""
        ...


class BaseReadService(
    BaseService,
    BaseListService,
    BaseRetriveService,
):
    """Базовый сервис для чтения."""

    pass


class BaseCrudService(
    BaseService,
    BaseCreateService,
    BaseListService,
    BaseRetriveService,
    BaseUpdateService,
    BaseDeleteService,
):
    """Базовый CRUD сервис."""

    pass


class ListService(BaseListService):
    """Получение списка элементов."""

    async def get_all(self, pagination: Paginator, ordering: Sequence[str]) -> list[BaseSchema]:
        """Получение списка элементов."""
        result = await self.repository.list_data(pagination.limit, pagination.offset, ordering)
        return [self.schema.model_validate(i) for i in result]


class RetriveService(BaseRetriveService):
    """Получение элемента по первичному ключу."""

    async def get_one(self, pk: PrimaryKey) -> BaseSchema:
        """Получение по первичному ключу."""
        result = await self.repository.retrive(pk)
        return self.schema.model_validate(result)


class CreateService(BaseCreateService):
    """Сервис создания."""

    async def create(self, creation_data: BaseSchema) -> BaseSchema:
        """Создание."""
        result = await self.repository.create(creation_data.model_dump())
        return self.schema.model_validate(result)


class UpdateService(BaseUpdateService):
    """Сервис обновления данных."""

    async def update(self, pk: PrimaryKey, update_data: BaseSchema) -> BaseSchema:
        """Обновление."""
        result = await self.repository.update(pk, update_data.model_dump())
        return self.schema.model_validate(result)


class DeleteService(BaseDeleteService):
    """Сервис удаления данных."""

    async def delete(self, pk: PrimaryKey) -> None:
        """Удаление."""
        await self.repository.delete(pk)


class CrudService(
    BaseService,
    ListService,
    RetriveService,
    CreateService,
    UpdateService,
    DeleteService,
):
    """CRUD сервис."""

    pass


class ReadService(
    BaseService,
    RetriveService,
    ListService,
):
    """Сервис для чтения."""

    pass
