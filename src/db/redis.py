from redis.asyncio import Redis


redis: Redis | None = None


async def get_redis() -> Redis | None:
    """Поулучение сессии для работы с кэшом."""
    return redis
