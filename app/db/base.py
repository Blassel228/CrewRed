import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core import settings

logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.INFO)

engine = create_async_engine(settings.db.url)
session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
