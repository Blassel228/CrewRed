from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.place import PlaceRepository
from app.repositories.project import ProjectRepository
from app.schemas.place import PlaceCreate, PlaceVisitedUpdate
from app.schemas.project import ProjectUpdate


class PlaceService:
    @staticmethod
    async def _validate_external_api(external_id: str):
        pass

    async def add_to_project(
        self, db: AsyncSession, place_repo: PlaceRepository, data: PlaceCreate
    ):
        existing_place = place_repo.get_one_or_none(
            filters={"project_id": data.project_id, "external_id": data.external_id},
            db=db,
        )
        if existing_place:
            raise HTTPException(
                status_code=409, detail="You are trying to add an existing place"
            )
        count_places = await place_repo.count_palces_for_project(
            project_id=data.project_id, db=db
        )
        if count_places >= 10:
            raise HTTPException(
                status_code=400, detail="Project can have maximum 10 places"
            )

        await self._validate_external_api(data.external_id)
        return await place_repo.add(db=db, data=data)

    async def get_all_for_project(
        self, db: AsyncSession, place_repo: PlaceRepository, project_id: UUID
    ):
        return await place_repo.get_many_or_none(db, {"project_id": project_id}) or []

    async def get_one_in_project(
        self,
        db: AsyncSession,
        place_repo: PlaceRepository,
        place_id: UUID,
        project_id: UUID,
    ):
        return await place_repo.get_one_or_none(
            db, {"id": place_id, "project_id": project_id}
        )

    async def update_visited(
        self,
        db: AsyncSession,
        place_repo: PlaceRepository,
        project_repo: ProjectRepository,
        place_id: UUID,
        project_id: UUID,
        data: PlaceVisitedUpdate,
    ):
        all_places = place_repo.get_many_or_none(
            db=db, filters={"project_id": project_id}
        )
        if all_places:
            needed_to_be_completed = len(all_places)
            visited = 0
            for place in all_places:
                if place.is_visited:
                    visited += 1
            if visited == needed_to_be_completed:
                await project_repo.update(
                    db=db,
                    filters={"id": project_id},
                    data=ProjectUpdate(is_completed=True),
                )

        return await place_repo.update(db=db, filters={"place_id": place_id}, data=data)
