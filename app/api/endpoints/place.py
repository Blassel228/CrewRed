from uuid import UUID

from fastapi import APIRouter

from app.api.dependencies import (
    unit_of_work_dep,
    place_service_dep,
    art_work_dep,
)
from app.schemas.place import PlaceCreate, PlaceVisitedUpdate, PlaceRead, PlaceCreateIn

router = APIRouter()


@router.post("/projects/{project_id}", response_model=PlaceRead)
async def add_place_to_project(
    project_id: UUID,
    data: PlaceCreateIn,
    unit_of_work: unit_of_work_dep,
    place_service: place_service_dep,
    art_work_service: art_work_dep,
):
    payload = PlaceCreate(**data.model_dump(), project_id=project_id)

    return await place_service.add_to_project(
        unit_of_work=unit_of_work,
        data=payload,
        art_work_service=art_work_service,
    )


@router.get("/projects/{project_id}", response_model=list[PlaceRead])
async def get_all_for_project(
    project_id: UUID,
    unit_of_work: unit_of_work_dep,
    service: place_service_dep,
):
    return await service.get_many_or_none(
        unit_of_work=unit_of_work,
        filters={"project_id": project_id},
    )


@router.get("/{place_id}", response_model=PlaceRead | None)
async def get_place_in_project(
    place_id: UUID,
    unit_of_work: unit_of_work_dep,
    service: place_service_dep,
):
    return await service.get_one(
        unit_of_work=unit_of_work,
        filters={"id": place_id},
    )


@router.patch("/{place_id}/visited", response_model=PlaceRead | None)
async def update_place_visited(
    place_id: UUID,
    data: PlaceVisitedUpdate,
    unit_of_work: unit_of_work_dep,
    service: place_service_dep,
):
    return await service.update_visited(
        unit_of_work=unit_of_work,
        place_id=place_id,
        data=data,
    )
