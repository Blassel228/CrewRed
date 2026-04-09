from app.core.config.base import BaseConfig
from app.core.config.db import DataBaseConfig


class Settings(BaseConfig):
    PROJECT_NAME: str = "test_backend"
    SERVER_HOST: str = "localhost"
    FRONTEND_URL: str = "http://localhost:5173/"
    SERVER_PORT: int = 8000
    SERVER_CORS_ORIGINS: str = "*"
    DEBUG: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    ALGORITHM: str
    SECRET: str
    ARTIC_BASE: str = "https://api.artic.edu/api/v1"

    db: DataBaseConfig = DataBaseConfig()

    @property
    def origins(self):
        return [origin.strip() for origin in self.SERVER_CORS_ORIGINS.split(",")]


settings = Settings()
