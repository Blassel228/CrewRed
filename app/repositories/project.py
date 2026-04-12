from select import select
from sqlalchemy import insert, Sequence
from sqlalchemy.orm import selectinload

from app.db.models import Place
from app.db.models.project import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository):
    model = Project

    # async def create_with_places(self, db, project_data: dict, places_data: list[dict]) -> Sequence[Project]:
    #     stmt = insert(self.model).values(**project_data).returning(Project.id)
    #     result = await db.execute(stmt)
    #     project_id = result.scalar_one()
    #
    #     if places_data:
    #         for p in places_data:
    #             p["project_id"] = project_id
    #         await db.execute(insert(Place).values(places_data))
    #
    #     await db.commit()
    #
    #     stmt = (
    #         select(self.model)
    #         .options(selectinload(Project.places))
    #         .where(self.model.id == project_id)
    #     )
    #     return (await db.execute(stmt)).scalars().first()
