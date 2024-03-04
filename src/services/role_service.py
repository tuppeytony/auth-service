from functools import lru_cache
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

from db.postgres import get_session
from models import RoleModel
from schemas import CreateRoleSchema
from schemas import RolesSchema
from schemas import SetUserRoleSchema
from schemas import UpdateRoleSchema
from utils.pagination import Paginator


class RoleService:
    """Сервис для ролей."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_roles(self, pagination: Paginator) -> list[RolesSchema]:
        """Получение всех ролей."""
        stmp = select(
            RoleModel.role_id,
            RoleModel.role_name,
        ).order_by(RoleModel.role_name).limit(pagination.limit).offset(pagination.offset)
        result = await self.session.scalars(stmp)
        return [RolesSchema.model_validate(role) for role in result.all()]

    async def get_role_by_id(self, role_id: UUID) -> RolesSchema:
        """Получение роли по id."""
        stmp = select(RoleModel).where(RoleModel.role_id == role_id)
        result = await self.session.execute(stmp)
        role = result.scalar_one_or_none()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Роли с таким id не существует',
            )
        return RolesSchema.model_validate(role)

    async def create_role(self, role: CreateRoleSchema) -> RolesSchema:
        """Создание роли."""
        try:
            new_role = RoleModel(**role.model_dump())
            self.session.add(new_role)
            await self.session.commit()
            await self.session.refresh(new_role)
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Роль с таким названием уже существует',
            )
        return RolesSchema.model_validate(new_role)

    async def update_role(self, role_id: UUID, updated_role: UpdateRoleSchema) -> RolesSchema:
        """Обновление роли по id."""
        try:
            stmp = update(
                RoleModel,
            ).where(
                RoleModel.role_id == role_id,
            ).values(**updated_role.model_dump()).returning(RoleModel)
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
        return RolesSchema.model_validate(updated_role)

    async def delete_role(self, role_id: UUID) -> None:
        """Удаление роли."""
        stmp = delete(RoleModel).where(RoleModel.role_id == role_id)
        await self.session.execute(stmp)
        await self.session.commit()

    async def set_user_role(self, user_role: SetUserRoleSchema) -> None:  # noqa: U100
        """Установка ролей пользователю."""
        ...


@lru_cache
def get_role_service(
    session: AsyncSession = Depends(get_session),
) -> RoleService:
    """Зависимость для сервиса ролей."""
    return RoleService(session)
