from abc import ABC

from repository import BaseRepository
from schemas.base_schema import BaseSchema


class BaseService(ABC):
    """интерфейс для сервисов."""

    read_schema: BaseSchema = None

    def __init__(self, repository: BaseRepository):
        self.repository = repository
