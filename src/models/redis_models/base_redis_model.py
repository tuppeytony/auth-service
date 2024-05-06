from aredis_om import HashModel

from db.redis import redis


class BaseRedisHashModel(HashModel):
    """Базовая модель для редис моделей."""

    class Meta:
        """."""

        database = redis
