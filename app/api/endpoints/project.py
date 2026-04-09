from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_dep, project_service_dep, project_repository_dep
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project import ProjectService

router = APIRouter()


@router.post("", response_model=ProjectRead)
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db_dep),
    repo: ProjectRepository = Depends(project_repository_dep),
    service: ProjectService = Depends(project_service_dep),
):
    return await service.add(db, repo, data)


@router.get("", response_model=list[ProjectRead])
async def get_projects(
    db: AsyncSession = Depends(get_db_dep),
    repo: ProjectRepository = Depends(project_repository_dep),
    service: ProjectService = Depends(project_service_dep),
):
    return await service.get_all(db, repo)


@router.get("/{project_id}", response_model=ProjectRead | None)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db_dep),
    repo: ProjectRepository = Depends(project_repository_dep),
    service: ProjectService = Depends(project_service_dep),
):
    return await service.get_one(db, repo, project_id)


@router.patch("/{project_id}", response_model=ProjectRead | None)
async def update_project(
    project_id: UUID,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db_dep),
    repo: ProjectRepository = Depends(project_repository_dep),
    service: ProjectService = Depends(project_service_dep),
):
    return await service.update(db, repo, project_id, data)


@router.delete("/{project_id}")
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db_dep),
    repo: ProjectRepository = Depends(project_repository_dep),
    service: ProjectService = Depends(project_service_dep),
):
    return await service.delete(db, repo, project_id)
