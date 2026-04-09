from uuid import UUID
from fastapi import APIRouter

from app.api.dependencies import get_db_dep, place_repository_dep, place_service_dep
from app.schemas.place import PlaceCreate, PlaceVisitedUpdate, PlaceRead

router = APIRouter()


@router.post("/projects/{project_id}", response_model=PlaceRead)
async def add_place_to_project(
    project_id: UUID,
    data: PlaceCreate,
    db: get_db_dep,
    repo: place_repository_dep,
    service: place_service_dep,
):
    data.project_id = project_id
    return await service.add_to_project(db, repo, data)


@router.get("/projects/{project_id}", response_model=list[PlaceRead])
async def get_places_for_project(
    project_id: UUID,
    db: get_db_dep,
    repo: place_repository_dep,
    service: place_service_dep,
):
    return await service.get_all_for_project(db, repo, project_id)


@router.get("/{place_id}/projects/{project_id}", response_model=PlaceRead | None)
async def get_place_in_project(
    place_id: UUID,
    project_id: UUID,
    db: get_db_dep,
    repo: place_repository_dep,
    service: place_service_dep,
):
    return await service.get_one_in_project(db, repo, place_id, project_id)


@router.patch("/{place_id}/visited", response_model=PlaceRead | None)
async def update_place_visited(
    place_id: UUID,
    data: PlaceVisitedUpdate,
    db: get_db_dep,
    repo: place_repository_dep,
    service: place_service_dep,
):
    return await service.update_visited(db, repo, place_id, data)
