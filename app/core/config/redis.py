from app.core.config.base import BaseConfig


class RedisBaseConfig(BaseConfig):
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
