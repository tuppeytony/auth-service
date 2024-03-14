from functools import lru_cache
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
from schemas import ClaimSchema
from schemas import CreateClaimSchema
from schemas import UpdateClaimSchema


class ClaimService:
    """Сервис свойств пользователя."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_claim(self, claim: CreateClaimSchema) -> ClaimSchema:
        """Создание свойства."""
        new_claim = ClaimModel(**claim.model_dump())
        self.session.add(new_claim)
        await self.session.commit()
        await self.session.refresh(new_claim)
        return ClaimSchema.model_validate(new_claim)

    async def get_user_claims(self, user_id: UUID) -> list[ClaimSchema]:
        """Получение свойств пользователя."""
        stmp = select(ClaimModel).where(ClaimModel.user_id == user_id)
        result = await self.session.execute(stmp)
        user_claims = result.scalars().all()
        return [ClaimSchema.model_validate(claim) for claim in user_claims]

    async def update_user_claim(self, user_id: UUID, update_claim: UpdateClaimSchema) -> UpdateClaimSchema:
        """Обновление свойства пользователя."""
        try:
            stmp = update(ClaimModel).where(
                ClaimModel.user_id == user_id,
                ClaimModel.claim_id == update_claim.claim_id,
            ).values(
                **update_claim.model_dump(exclude={'claim_id', 'user_id'}),
            ).returning(ClaimModel)
            result = await self.session.execute(stmp)
            await self.session.commit()
            updated_claim = result.scalar_one()
        except NoResultFound:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Такого свойства у пользователя нет',
            )
        return UpdateClaimSchema.model_validate(updated_claim)

    async def delete_user_claim(self, user_id: UUID, claim_id: UUID) -> None:
        """Удаление свойства пользователя."""
        stmp = delete(ClaimModel).where(
            ClaimModel.user_id == user_id,
            ClaimModel.claim_id == claim_id,
        )
        await self.session.execute(stmp)
        await self.session.commit()


@lru_cache
def get_claim_service(session: AsyncSession = Depends(get_session)) -> ClaimService:
    """Получение сервиса свойств пользователя."""
    return ClaimService(session)
