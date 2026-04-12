from pydantic import Field

from app.core.config.base import BaseConfig


class DataBaseConfig(BaseConfig):
    USER: str = Field(..., alias="DB_USER")
    PASSWORD: str = Field(..., alias="DB_PASS")
    HOST: str = Field(..., alias="DB_HOST")
    PORT: str = Field(..., alias="DB_PORT")
    NAME: str = Field(..., alias="DB_NAME")

    @property
    def url(self) -> str:
        """Constructs the SQLAlchemy URL using the database configuration."""
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

    @property
    def alembic_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}"
            f"@localhost:{self.PORT}/{self.NAME}"
        )
