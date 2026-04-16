import redis.asyncio as redis

from app.core.config.config import settings

redis_client = redis.Redis(
    host=settings.redis.REDIS_HOST,
    port=settings.redis.REDIS_PORT,
    db=0,
    decode_responses=True,
)
