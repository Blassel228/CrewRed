from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.place import PlaceRepository
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectCreateWithPlaces


class ProjectService:
    async def add(
        self,
        db: AsyncSession,
        repo: ProjectRepository,
        data: ProjectCreate,
    ):
        return await repo.add(db, data)

    async def create_with_places(
        self,
        db: AsyncSession,
        repo: ProjectRepository,
        data: ProjectCreateWithPlaces,
        user_id: UUID,
    ):
        if not (1 <= len(data.places) <= 10):
            raise ValueError("Project must contain between 1 and 10 places.")

        places_data = [p.model_dump() for p in data.places]

        project_data = data.model_dump(exclude={"places"})
        project_data["user_id"] = user_id

        return await repo.create_with_places(db, project_data, places_data)

    async def get_one(
        self,
        db: AsyncSession,
        repo: ProjectRepository,
        project_id: UUID,
    ):
        return await repo.get_one(db, {"id": project_id})

    async def get_all(
        self,
        db: AsyncSession,
        repo: ProjectRepository,
    ):
        return await repo.get_many_or_none(db) or []

    async def update(
        self,
        db: AsyncSession,
        repo: ProjectRepository,
        project_id: UUID,
        data: ProjectUpdate,
    ):
        return await repo.update(db, {"id": project_id}, data)

    async def delete(
        self,
        db: AsyncSession,
        project_repo: ProjectRepository,
        place_repo: PlaceRepository,
        project_id: UUID,
    ):
        has_visited = await place_repo.get_many_or_none(filters={"project_id": project_id, "is_visited": True}, db=db)
        if has_visited:
            raise HTTPException(
                status_code=409,
                detail="Cannot delete project because some places have been visited"
            )
        return await project_repo.delete(db, {"id": project_id})
