from uuid import UUID

from fastapi import APIRouter, Query

from app.api.dependencies import (
    project_service_dep,
    get_current_user,
    art_work_dep,
    unit_of_work_dep,
)
from app.schemas.project import (
    ProjectRead,
    ProjectUpdate,
    ProjectCreateWithPlacesIn,
    ProjectCreateIn,
)

router = APIRouter()


@router.post("", response_model=ProjectRead)
async def create_project(
    data: ProjectCreateIn,
    user: get_current_user,
    service: project_service_dep,
    unit_of_work: unit_of_work_dep,
):
    return await service.add(
        unit_of_work=unit_of_work,
        data=data,
        user_id=user.id,
    )


@router.post("/create-with-places", response_model=ProjectRead)
async def create_with_places(
    data: ProjectCreateWithPlacesIn,
    user: get_current_user,
    project_service: project_service_dep,
    art_work_service: art_work_dep,
    unit_of_work: unit_of_work_dep,
):
    return await project_service.create_with_places(
        unit_of_work=unit_of_work,
        data=data,
        user_id=user.id,
        art_work_service=art_work_service,
    )


@router.get("", response_model=list[ProjectRead])
async def get_projects(
    service: project_service_dep,
    unit_of_work: unit_of_work_dep,
    limit: int = Query(10),
    offset: int = Query(0),
):
    return await service.get_many(
        unit_of_work=unit_of_work,
        limit=limit,
        offset=offset,
    )


@router.get("/{project_id}", response_model=ProjectRead | None)
async def get_project(
    project_id: UUID,
    service: project_service_dep,
    unit_of_work: unit_of_work_dep,
):
    return await service.get_one(
        unit_of_work=unit_of_work,
        filters={"id": project_id},
    )


@router.patch("/{project_id}", response_model=ProjectRead | None)
async def update_project(
    project_id: UUID,
    data: ProjectUpdate,
    service: project_service_dep,
    unit_of_work: unit_of_work_dep,
):
    return await service.update(
        unit_of_work=unit_of_work,
        filters={"id": project_id},
        data=data,
    )


@router.delete("/{project_id}")
async def delete_project(
    project_id: UUID,
    service: project_service_dep,
    unit_of_work: unit_of_work_dep,
):
    return await service.delete(
        unit_of_work=unit_of_work,
        project_id=project_id,
    )
