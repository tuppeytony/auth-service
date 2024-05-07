from functools import lru_cache
from typing import Any
from typing import Sequence
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func

from db.postgres import get_session
from models import AuthUserModel
from models import RoleAuthUserAssociation
from models import RoleModel
from schemas import SetUserRoleSchema
from utils.consts import PrimaryKey

from .base_repository import CrudRepository


class RolesRepository(CrudRepository):
    """Репозиторий для ролей."""

    model = RoleModel

    async def update(self, pk: PrimaryKey, update_data: dict) -> Any:
        """Обновление роли по id."""
        try:
            stmp = update(
                self.model,
            ).where(
                self.model.role_id == pk,
                self.model.role_name != self.model.admin_role,
            ).values(**update_data).returning(self.model)
            result = await self.session.execute(stmp)
            updated_role = result.scalar_one()
        except NoResultFound:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Такой роли не существует',
            )
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Такая роль уже существует',
            )
        return updated_role

    async def delete(self, pk: PrimaryKey) -> None:
        """Удаление роли."""
        stmp = delete(self.model).where(
            self.model.role_id == pk,
            self.model.role_name != self.model.admin_role,
        )
        await self.session.execute(stmp)
        await self.session.commit()

    async def user_roles(self, user_id: UUID) -> Any:
        """Получение ролей пользователя."""
        stmp = select(
            func.array_agg(self.model.role_name).label('roles'),
        ).join(
            RoleAuthUserAssociation,
        ).join(
            AuthUserModel,
        ).where(AuthUserModel.auth_user_id == user_id)
        result = await self.session.execute(stmp)
        return result.scalar()

    async def set_user_role(self, user_role: SetUserRoleSchema) -> None:
        """Установка ролей пользователю."""
        roles: list | Sequence[RoleModel] = []
        user_stmp = select(AuthUserModel).where(
            AuthUserModel.auth_user_id == user_role.user_id,
        ).options(selectinload(AuthUserModel.roles))
        user_result = await self.session.execute(user_stmp)
        user = user_result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Такого пользователя не существует',
            )
        if user_role.roles_id:
            roles_stmp = select(RoleModel).where(
                RoleModel.role_id.in_(user_role.roles_id),
                RoleModel.role_name != RoleModel.admin_role,
            )
            roles_result = await self.session.execute(roles_stmp)
            roles = roles_result.scalars().all()
            if not roles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Таких ролей нет',
                )
        if user.roles != roles:
            user.roles = roles
            await self.session.commit()


@lru_cache
def get_role_repo(
    session: AsyncSession = Depends(get_session),
) -> RolesRepository:
    """Получение репозитория ролей."""
    return RolesRepository(session)
