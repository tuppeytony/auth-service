from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.config import app_settings
from models import AuthUserModel
from models import RoleModel
from schemas import UserRegisterSchema


class CreateAdmin:
    """Создание администратора и роли администратора."""

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def __create_admin_role(self, session: AsyncSession) -> None:
        stmp = select(RoleModel).where(RoleModel.role_name == RoleModel.admin_role)
        result = await session.execute(stmp)
        admin_role = result.scalar_one_or_none()
        if not admin_role:
            create_admin_role = RoleModel(RoleModel.admin_role)
            session.add(create_admin_role)
            await session.commit()

    async def __is_admin_exists(self, session: AsyncSession) -> tuple[bool, RoleModel]:
        stmp = select(RoleModel).where(
            RoleModel.role_name == RoleModel.admin_role,
        ).options(
            selectinload(RoleModel.users),
        )
        result = await session.execute(stmp)
        admin_role = result.scalar_one()
        return bool(admin_role.users), admin_role

    async def __create_admin(self, session: AsyncSession) -> None:
        is_admin_exists, admin_role = await self.__is_admin_exists(session)
        if app_settings.admin_email and app_settings.admin_password and not is_admin_exists:
            try:
                validate_admin_user = UserRegisterSchema(
                    email=app_settings.admin_email,
                    password=app_settings.admin_password,
                )
                admin_user = AuthUserModel(**validate_admin_user.model_dump())
                session.add(admin_user)
                await session.commit()
                await session.refresh(admin_user, ('roles', ))
                admin_user.roles.append(admin_role)
                await session.commit()
            except ValidationError:
                pass

    async def create_admin(self) -> None:
        """Создание администратора."""
        async with self.async_session() as session:  # type: ignore
            await self.__create_admin_role(session)
            await self.__create_admin(session)
