from uuid import UUID

from sqlalchemy import select, func

from app.db.models.place import Place
from app.repositories.base import BaseRepository


class PlaceRepository(BaseRepository):
    model = Place

    async def count_places_for_project(self, project_id: UUID) -> int:
        stmt = select(func.count(Place.id)).where(Place.project_id == project_id)
        return await self.session.scalar(stmt) or 0
