from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import Sequence

from app.db.models import Project
from app.redis.redis_client import redis_client
from app.schemas.place import PlaceCreate
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectCreateIn,
    ProjectCreateWithPlacesIn,
)
from app.services.artworkApi import ArtworkApiService
from app.utils.unit_of_work import UnitOfWork


class ProjectService:
    async def add(
        self,
        unit_of_work: UnitOfWork,
        user_id: UUID,
        data: ProjectCreateIn,
    ) -> Sequence[Project]:
        async with unit_of_work:
            payload = ProjectCreate(**data.model_dump(), user_id=user_id)
            return await unit_of_work.project.add(payload)

    async def create_with_places(
        self,
        unit_of_work: UnitOfWork,
        data: ProjectCreateWithPlacesIn,
        art_work_service: ArtworkApiService,
        user_id: UUID,
    ):
        if not (1 <= len(data.places) <= 10):
            raise HTTPException(
                status_code=409, detail="Project must contain between 1 and 10 places."
            )

        if len(data.places) == 10:
            data.is_completed = True

        seen = set()
        for place in data.places:
            if place.external_id in seen:
                raise HTTPException(
                    status_code=409, detail="You cannot add same places to the list."
                )
            seen.add(place.external_id)

            cache_key = f"place:{place.external_id}"
            cached = await redis_client.get(cache_key)

            if not cached:
                exists = await art_work_service.get_place_by_external_id(
                    place.external_id
                )
                if not exists:
                    raise HTTPException(
                        status_code=404, detail="The place was not found."
                    )
                await redis_client.set(cache_key, "cached", ex=3600)

        payload = data.model_dump()
        places_payload = payload.pop("places")

        async with unit_of_work:
            project = await unit_of_work.project.add(
                ProjectCreate(**payload, user_id=user_id)
            )

            for place in places_payload:
                await unit_of_work.place.add(
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
        unit_of_work: UnitOfWork,
        filters: dict[str, any] | None = None,
    ) -> Sequence[Project]:
        async with unit_of_work:
            return await unit_of_work.project.get_one(filters)

    async def get_many(
        self,
        unit_of_work: UnitOfWork,
        filters: dict[str, any] | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> Sequence[Project]:
        async with unit_of_work:
            return await unit_of_work.project.get_many(
                limit=limit, offset=offset, filters=filters
            )

    async def update(
        self,
        unit_of_work: UnitOfWork,
        filters: dict[str, any],
        data: ProjectUpdate,
    ) -> Sequence[Project]:
        async with unit_of_work:
            return await unit_of_work.project.update(filters, data)

    async def delete(
        self,
        unit_of_work: UnitOfWork,
        project_id: UUID,
    ) -> bool:
        async with unit_of_work:
            has_visited = await unit_of_work.place.get_many_or_none(
                {"project_id": project_id, "is_visited": True}
            )

            if has_visited:
                raise HTTPException(
                    status_code=409,
                    detail="Cannot delete project because some places have been visited",
                )

            return await unit_of_work.project.delete({"id": project_id})
