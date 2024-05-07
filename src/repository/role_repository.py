from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models import RoleModel

from .base_repository import CrudRepository


class RolesRepository(CrudRepository):
    """Репозиторий для ролей."""

    model = RoleModel


@lru_cache
def get_role_repo(
    session: AsyncSession = Depends(get_session),
) -> RolesRepository:
    """Получение репозитория ролей."""
    return RolesRepository(session)
