from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from repository import BaseRepository
from repository import get_claim_repo
from schemas import ClaimSchema
from schemas import UpdateClaimSchema

from .base_service import BaseService
from .base_service import CreateService


class ClaimService(BaseService, CreateService):
    """Сервис свойств пользователя."""

    schema = ClaimSchema

    async def get_user_claims(self, user_id: UUID) -> list[ClaimSchema]:
        """Получение свойств пользователя."""
        user_claims = await self.repository.get_user_claims(user_id)
        return [self.schema.model_validate(claim) for claim in user_claims]

    async def update_user_claim(self, user_id: UUID, update_claim: UpdateClaimSchema) -> UpdateClaimSchema:
        """Обновление свойства пользователя."""
        updated_claim = await self.repository.update_user_claim(
            user_id,
            update_claim.claim_id,
            update_claim.model_dump(exclude={'claim_id', 'user_id'}),
        )
        return UpdateClaimSchema.model_validate(updated_claim)

    async def delete_user_claim(self, user_id: UUID, claim_id: UUID) -> None:
        """Удаление свойства пользователя."""
        await self.repository.delete_user_claim(user_id, claim_id)


@lru_cache
def get_claim_service(
    repository: BaseRepository = Depends(get_claim_repo),
) -> ClaimService:
    """Получение сервиса свойств пользователя."""
    return ClaimService(repository)
