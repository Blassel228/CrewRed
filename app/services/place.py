import json
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Place
from app.redis.redis_client import redis_client
from app.repositories.place import PlaceRepository
from app.repositories.project import ProjectRepository
from app.schemas.place import PlaceCreate, PlaceVisitedUpdate
from app.schemas.project import ProjectUpdate
from app.services.artworkApi import ArtworkApiService


class PlaceService:
    async def add_to_project(
        self,
        db: AsyncSession,
        repo: PlaceRepository,
        art_work_service: ArtworkApiService,
        data: PlaceCreate
    ) -> Sequence[Place]:

        existing_place = await repo.get_one_or_none(
            filters={"project_id": data.project_id, "external_id": data.external_id},
            db=db,
        )
        if existing_place:
            raise HTTPException(
                status_code=409, detail="You are trying to add an existing place"
            )

        cache_key = f"place:{data.external_id}"

        cached = await redis_client.get(cache_key)
        if cached:
            return await repo.add(db=db, data=data)

        place_from_api = await art_work_service.get_place_by_external_id(data.external_id)
        if not place_from_api:
            raise HTTPException(status_code=404, detail="The place was not found.")

        await redis_client.set(cache_key, json.dumps(place_from_api), ex=3600)

        count_places = await repo.count_palces_for_project(
            project_id=data.project_id, db=db
        )
        if count_places >= 10:
            raise HTTPException(
                status_code=400, detail="Project can have maximum 10 places"
            )

        return await repo.add(db=db, data=data)

    async def get_many_or_none(
        self,
        filters: dict[str, any],
        db: AsyncSession,
        repo: PlaceRepository,
    ) -> Sequence[Place]:
        return await repo.get_many_or_none(db, filters) or []

    async def get_one(
        self,
        filters: dict[str, any],
        db: AsyncSession,
        repo: PlaceRepository,
    ) -> Sequence[Place]:
        return await repo.get_one(db=db, filters=filters)

    async def update_visited(
        self,
        db: AsyncSession,
        place_repo: PlaceRepository,
        project_repo: ProjectRepository,
        place_id: UUID,
        data: PlaceVisitedUpdate,
    ) -> Sequence[Place]:
        place = await place_repo.get_one(filters={"id": place_id}, db=db)
        project_id = place.project_id
        all_places = await place_repo.get_many_or_none(
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
        res = await place_repo.update(db=db, filters={"id": place_id}, data=data)
        return res
