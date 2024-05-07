# mypy: disable-error-code="attr-defined"
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from fastapi import status
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession


PrimaryKey = UUID | str | int


class BaseRepositoryMixin:
    """Базовый миксин для репозитория."""

    model: Any = None

    def __init__(self, session: AsyncSession):
        self.session = session


class BaseCreateRepository(ABC):
    """интерфейс для создания записи в БД."""

    @abstractmethod
    async def create(self, creation_data: dict) -> Any:  # noqa: U100
        """Метод для создания записи в БД."""
        ...


class BaseUpdateRepository(ABC):
    """Базовый класс для обновления данных в БД."""

    @abstractmethod
    async def update(self, pk: PrimaryKey, update_data: dict) -> Any:  # noqa: U100
        """Метод для обновления записи в БД."""
        ...


class BaseDeleteRepository(ABC):
    """Базовый класс для удаление записи из БД."""

    @abstractmethod
    async def delete(self, pk: PrimaryKey) -> None:  # noqa: U100
        """Метод для удаления записи в БД."""
        ...


class BaseRetriveRepository(ABC):
    """Базовый класс для получения по первичному ключу данных из БД."""

    @abstractmethod
    async def retrive(self, pk: PrimaryKey) -> Any | None:  # noqa: U100
        """Получение записи из БД по первичному ключу."""
        ...


class BaseListRepository(ABC):
    """Базовый класс для получения данных с ограничением по количеству записей, оффсета и с сортирокой из БД."""

    @abstractmethod
    async def list_data(
        self,
        limit: int,  # noqa: U100
        offset: int,  # noqa: U100
        order_by: Sequence[str],  # noqa: U100
    ) -> Any | None:
        """Получение данных с ограничением по количеству записей, оффсета и с сортирокой из БД."""
        ...


class RetriveRepositoryMixin(BaseRetriveRepository):
    """Получение записи по первичному ключу из БД."""

    async def retrive(self, pk: PrimaryKey) -> Any | None:
        """Получение записи из БД по первичному ключу."""
        stmp = select(self.model).where(self.model.pk == pk)
        result = await self.session.execute(stmp)
        return result.scalar_one_or_none()


class ListRepositoryMixin(BaseListRepository):
    """Получение данных с ограничением по количеству записей, оффсета и с сортирокой из БД."""

    async def list_data(
        self,
        limit: int,
        offset: int,
        order_by: Sequence[str],
    ) -> Any | None:
        """Получение данных с ограничением по количеству записей, оффсета и с сортирокой из БД."""
        stmp = select(self.model).order_by(*order_by).limit(limit).offset(offset)
        result = await self.session.execute(stmp)
        return result.all()


class CreateRepositoryMixin(BaseCreateRepository):
    """Создание записи в БД."""

    async def create(self, creation_data: dict) -> Any:
        """Создание записи в БД."""
        try:
            new_data = self.model(**creation_data)
            self.session.add(new_data)
            await self.session.commit()
            await self.session.refresh(new_data)
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'{self.model.__tablename__} с таким названием уже существует',
            )
        return new_data


class UpdateRepositoryMixin(BaseUpdateRepository):
    """Обновление записи в БД."""

    async def update(self, pk: PrimaryKey, update_data: dict) -> Any:
        """Обновление записи с БД."""
        try:
            stmp = update(self.model).where(self.model.pk == pk).values(
                **update_data,
            ).returning(self.model)
            result = await self.session.execute(stmp)
            await self.session.commit()
            updated_data = result.scalar_one()
        except NoResultFound:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Такого свойства у {self.model.__tablename__} нет',
            )
        return updated_data


class DeleteRepositoryMixin(BaseDeleteRepository):
    """Удаление записи из БД."""

    async def delete(self, pk: PrimaryKey) -> None:
        """Удаление записи из БД."""
        stmp = delete(self.model).where(
            self.model.pk == pk,
        )
        await self.session.execute(stmp)
        await self.session.commit()


class CrudRepository(
    BaseRepositoryMixin,
    CreateRepositoryMixin,
    RetriveRepositoryMixin,
    UpdateRepositoryMixin,
    DeleteRepositoryMixin,
    ListRepositoryMixin,
):
    """Реализация CRUD репозитория."""

    pass


class ReadOnlyRepository(
    BaseRepositoryMixin,
    RetriveRepositoryMixin,
    ListRepositoryMixin,
):
    """Реализация репозитория только для чтения."""

    pass
