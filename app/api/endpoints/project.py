from uuid import UUID

from fastapi import APIRouter, Query

from app.api.dependencies import (
    get_db_dep,
    project_service_dep,
    project_repository_dep,
    place_repository_dep,
    get_current_user,
    art_work_dep
)
from app.schemas.project import (
    ProjectRead,
    ProjectUpdate,
    ProjectCreateWithPlacesIn, ProjectCreateIn,
)

router = APIRouter()


@router.post("", response_model=ProjectRead)
async def create_project(
    data: ProjectCreateIn,
    db: get_db_dep,
    user: get_current_user,
    repo: project_repository_dep,
    service: project_service_dep,
):
    return await service.add(db=db, repo=repo, data=data, user_id=user.id)


@router.post("/create-with-places", response_model=ProjectRead)
async def create_with_places(
    data: ProjectCreateWithPlacesIn,
    db: get_db_dep,
    user: get_current_user,
    project_repo: project_repository_dep,
    place_repo: place_repository_dep,
    project_service: project_service_dep,
    art_work_service: art_work_dep
):
    return await project_service.create_with_places(
        db=db, repo=project_repo, data=data, user_id=user.id, art_work_service=art_work_service, place_repo=place_repo
    )


@router.get("", response_model=list[ProjectRead])
async def get_projects(
    db: get_db_dep,
    repo: project_repository_dep,
    service: project_service_dep,
    limit: int = Query(10),
    offset: int = Query(0),
):
    return await service.get_many(db=db, repo=repo, limit=limit, offset=offset)


@router.get("/{project_id}", response_model=ProjectRead | None)
async def get_project(
    project_id: UUID,
    db: get_db_dep,
    repo: project_repository_dep,
    service: project_service_dep,
):
    return await service.get_one(db=db, filters={"id": project_id}, repo=repo)


@router.patch("/{project_id}", response_model=ProjectRead | None)
async def update_project(
    project_id: UUID,
    data: ProjectUpdate,
    db: get_db_dep,
    repo: project_repository_dep,
    service: project_service_dep,
):
    return await service.update(db=db, repo=repo, filters={"id": project_id}, data=data)


@router.delete("/{project_id}")
async def delete_project(
    project_id: UUID,
    db: get_db_dep,
    project_repo: project_repository_dep,
    place_repo: place_repository_dep,
    service: project_service_dep,
):
    return await service.delete(db, project_repo, place_repo, project_id)
