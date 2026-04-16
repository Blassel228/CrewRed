import json
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import Sequence

from app.db.models import Place
from app.redis.redis_client import redis_client
from app.schemas.place import PlaceCreate, PlaceVisitedUpdate
from app.schemas.project import ProjectUpdate
from app.services.artworkApi import ArtworkApiService
from app.utils.unit_of_work import UnitOfWork


class PlaceService:
    async def add_to_project(
        self,
        unit_of_work: UnitOfWork,
        art_work_service: ArtworkApiService,
        data: PlaceCreate,
    ) -> Sequence[Place]:

        async with unit_of_work:
            existing_place = await unit_of_work.place.get_one_or_none(
                filters={"project_id": data.project_id, "external_id": data.external_id}
            )

        if existing_place:
            raise HTTPException(
                status_code=409, detail="You are trying to add an existing place"
            )

        cache_key = f"place:{data.external_id}"
        cached = await redis_client.get(cache_key)

        if cached:
            return await unit_of_work.place.add(data=data)

        place_from_api = await art_work_service.get_place_by_external_id(
            data.external_id
        )

        if not place_from_api:
            raise HTTPException(status_code=404, detail="The place was not found.")

        await redis_client.set(cache_key, json.dumps(place_from_api), ex=3600)

        async with unit_of_work:
            count_places = await unit_of_work.place.count_places_for_project(
                project_id=data.project_id
            )

            if count_places >= 10:
                raise HTTPException(
                    status_code=400, detail="Project can have maximum 10 places"
                )

            return await unit_of_work.place.add(data=data)

    async def get_many_or_none(
        self,
        unit_of_work: UnitOfWork,
        filters: dict[str, any],
    ) -> Sequence[Place]:
        async with unit_of_work:
            return await unit_of_work.place.get_many_or_none(filters) or []

    async def get_one(
        self,
        unit_of_work: UnitOfWork,
        filters: dict[str, any],
    ) -> Place:
        async with unit_of_work:
            return await unit_of_work.place.get_one(filters=filters)

    async def update_visited(
        self,
        unit_of_work: UnitOfWork,
        place_id: UUID,
        data: PlaceVisitedUpdate,
    ) -> Sequence[Place]:

        async with unit_of_work:
            place = await unit_of_work.place.get_one({"id": place_id})
            project_id = place.project_id

            all_places = await unit_of_work.place.get_many_or_none(
                {"project_id": project_id}
            )

        async with unit_of_work:
            if all_places:
                needed_to_be_completed = len(all_places)
                visited = sum(1 for p in all_places if p.is_visited)

                if visited == needed_to_be_completed:
                        await unit_of_work.project.update(
                            filters={"id": project_id},
                            data=ProjectUpdate(is_completed=True),
                        )
            return await unit_of_work.place.update(filters={"id": place_id}, data=data)
