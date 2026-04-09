from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.place import Place
from app.repositories.base import BaseRepository


class PlaceRepository(BaseRepository):
    model = Place

    async def count_palces_for_project(self, db: AsyncSession, project_id: UUID):
        stmt = select(func.count(Place.id)).where(Place.project_id == project_id)
        return await db.scalar(stmt) or 0
