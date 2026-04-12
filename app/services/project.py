from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Project
from app.redis.redis_client import redis_client
from app.repositories.place import PlaceRepository
from app.repositories.project import ProjectRepository
from app.schemas.place import PlaceCreate
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectCreateIn,
    ProjectCreateWithPlacesIn,
)
from app.services.artworkApi import ArtworkApiService


class ProjectService:
    async def add(
        self,
        db: AsyncSession,
        user_id: UUID,
        repo: ProjectRepository,
        data: ProjectCreateIn,
    ) -> Sequence[Project]:
        data = ProjectCreate(**data.model_dump(), user_id=user_id)
        return await repo.add(db, data)

    async def create_with_places(
            self,
            db: AsyncSession,
            repo: ProjectRepository,
            place_repo: PlaceRepository,
            data: ProjectCreateWithPlacesIn,
            art_work_service: ArtworkApiService,
            user_id: UUID,
    ):

        if not (1 <= len(data.places) <= 10):
            raise HTTPException(
                status_code=409,
                detail="Project must contain between 1 and 10 places."
            )
        if len(data.places) == 10:
            data.is_completed = True

        seen = set()
        for place in data.places:
            if place.external_id in seen:
                raise HTTPException(
                    status_code=409,
                    detail="You cannot add same places to the list."
                )
            seen.add(place.external_id)

            cache_key = f"place:{place.external_id}"

            cached = await redis_client.get(cache_key)
            if not cached:
                exists = await art_work_service.get_place_by_external_id(place.external_id)
                if not exists:
                    raise HTTPException(status_code=404, detail="The place was not found.")
                await redis_client.set(cache_key, "cached", ex=3600)

        payload = data.model_dump()
        places_payload = payload.pop("places")

        project = await repo.add(
            db,
            ProjectCreate(
                **payload,
                user_id=user_id
            )
        )

        for place in places_payload:
            await place_repo.add(
                db,
                PlaceCreate(
                    project_id=project.id,
                    external_id=place["external_id"],
                    name=place["name"],
                    longitude=place.get("longitude"),
                    latitude=place.get("latitude"),
                )
            )

        return project

    async def get_one(
        self,
        db: AsyncSession,
        repo: ProjectRepository,
        filters: dict[str, any] | None = None,
    ) -> Sequence[Project]:
        return await repo.get_one(db, filters)

    async def get_many(
        self,
        db: AsyncSession,
        repo: ProjectRepository,
        filters: dict[str, any] | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> Sequence[Project]:
        return await repo.get_many(db=db, limit=limit, offset=offset, filters=filters)

    async def update(
        self,
        db: AsyncSession,
        repo: ProjectRepository,
        filters: dict[str, any],
        data: ProjectUpdate,
    ) -> Sequence[Project]:
        return await repo.update(db, filters, data)

    async def delete(
        self,
        db: AsyncSession,
        project_repo: ProjectRepository,
        place_repo: PlaceRepository,
        project_id: UUID,
    ) -> bool:
        has_visited = await place_repo.get_many_or_none(
            filters={"project_id": project_id, "is_visited": True}, db=db
        )
        if has_visited:
            raise HTTPException(
                status_code=409,
                detail="Cannot delete project because some places have been visited",
            )
        return await project_repo.delete(db, {"id": project_id})
