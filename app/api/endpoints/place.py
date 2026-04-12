from uuid import UUID
from fastapi import APIRouter

from app.api.dependencies import get_db_dep, place_repository_dep, place_service_dep, art_work_dep, project_repository_dep
from app.schemas.place import PlaceCreate, PlaceVisitedUpdate, PlaceRead, PlaceCreateIn

router = APIRouter()


@router.post("/projects/{project_id}", response_model=PlaceRead)
async def add_place_to_project(
    project_id: UUID,
    data: PlaceCreateIn,
    db: get_db_dep,
    repo: place_repository_dep,
    place_service: place_service_dep,
    art_work_service:art_work_dep
):
    data = PlaceCreate(**data.model_dump(), project_id=project_id)
    return await place_service.add_to_project(db=db, repo=repo, data=data, art_work_service=art_work_service)


@router.get("/projects/{project_id}", response_model=list[PlaceRead])
async def get_all_for_project(
    project_id: UUID,
    db: get_db_dep,
    repo: place_repository_dep,
    service: place_service_dep,
):
    return await service.get_many_or_none(
        db=db, repo=repo, filters={"project_id": project_id}
    )


@router.get("/{place_id}", response_model=PlaceRead | None)
async def get_place_in_project(
    place_id: UUID,
    db: get_db_dep,
    repo: place_repository_dep,
    service: place_service_dep,
):
    return await service.get_one(
        db=db, repo=repo, filters={"id": place_id}
    )


@router.patch("/{place_id}/visited", response_model=PlaceRead | None)
async def update_place_visited(
    place_id: UUID,
    data: PlaceVisitedUpdate,
    db: get_db_dep,
    place_repo: place_repository_dep,
    project_repo: project_repository_dep,
    service: place_service_dep,
):
    return await service.update_visited(db=db, place_repo=place_repo, project_repo=project_repo, data=data, place_id=place_id)
