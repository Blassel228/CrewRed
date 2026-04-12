from app.db.base import session


async def get_db():
    async with session() as db:
        async with db.begin():
            yield db
