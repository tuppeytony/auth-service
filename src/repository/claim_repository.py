from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models import ClaimModel

from .base_repository import BaseRepository
from .base_repository import CreateRepositoryMixin


class ClaimRepository(BaseRepository, CreateRepositoryMixin):
    """Репозиторий свойств."""

    model = ClaimModel

    async def get_user_claims(self, user_id: UUID) -> Any:
        """Получение свойств пользователя."""
        stmp = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmp)
        return result.scalars().all()

    async def update_user_claim(self, user_id: UUID, claim_id: UUID, update_data: dict) -> Any:
        """Обновление свойства пользователя."""
        try:
            stmp = update(self.model).where(
                self.model.user_id == user_id,
                self.model.claim_id == claim_id,
            ).values(
                **update_data,
            ).returning(self.model)
            result = await self.session.execute(stmp)
            await self.session.commit()
            updated_claim = result.scalar_one()
        except NoResultFound:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Такого свойства у пользователя нет',
            )
        return updated_claim

    async def delete_user_claim(self, user_id: UUID, claim_id: UUID) -> None:
        """Удаление свойства пользователя."""
        stmp = delete(self.model).where(
            self.model.user_id == user_id,
            self.model.claim_id == claim_id,
        )
        await self.session.execute(stmp)
        await self.session.commit()


@lru_cache
def get_claim_repo(
    session: AsyncSession = Depends(get_session),
) -> ClaimRepository:
    """Получение репозитория свойств."""
    return ClaimRepository(session)
