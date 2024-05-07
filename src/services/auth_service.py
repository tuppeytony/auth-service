from functools import lru_cache

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from models import AuthUserModel
from repository import BaseRepository
from repository import get_auth_repo
from schemas import UserRegisterSchema

from .base_service import BaseService


class AuthService(BaseService):
    """Сервис аутентификаций."""

    schema = UserRegisterSchema

    async def register(self, user: UserRegisterSchema) -> str:
        """Регистрация пользователя."""
        new_user = await self.repository.register(user.model_dump())
        return str(new_user.auth_user_id)

    async def login(self, user: UserRegisterSchema) -> str:
        """Вход пользователя в систему."""
        auth_user = await self.repository.login(user.email)
        self.__validate_user(auth_user, user)
        return str(auth_user.auth_user_id)

    def __validate_user(self, auth_user: AuthUserModel, user: UserRegisterSchema) -> None:
        """Проверка пользователя при входе."""
        if not auth_user.check_user_hash_password(user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Неправильный пароль',
            )


@lru_cache
def get_auth_service(
    repository: BaseRepository = Depends(get_auth_repo),
) -> AuthService:
    """Получение сервиса аутентификаций."""
    return AuthService(repository)
