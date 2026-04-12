from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies import (
    get_db_dep,
    user_service_dep,
    user_repository_dep,
    auth_service_dep,
    get_current_user,
)
from app.schemas.user import UserCreateIn, UserUpdateIn, UserRead

router = APIRouter()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreateIn,
    db: get_db_dep,
    repo: user_repository_dep,
    auth_service: auth_service_dep,
    service: user_service_dep,
):
    return await service.add(
        data=data,
        auth_service=auth_service,
        repo=repo,
        db=db,
    )


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    data: UserUpdateIn,
    db: get_db_dep,
    repo: user_repository_dep,
    auth_service: auth_service_dep,
    service: user_service_dep,
):
    return await service.update(
        user_id=user_id,
        data=data,
        auth_service=auth_service,
        repo=repo,
        db=db,
    )


@router.put("/self-update", response_model=UserRead)
async def update_user(
    user: get_current_user,
    data: UserUpdateIn,
    db: get_db_dep,
    repo: user_repository_dep,
    auth_service: auth_service_dep,
    service: user_service_dep,
):
    return await service.update(
        user_id=user.id,
        data=data,
        auth_service=auth_service,
        repo=repo,
        db=db,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: get_db_dep,
    repo: user_repository_dep,
    service: user_service_dep,
):
    await service.delete(
        user_id=user_id,
        repo=repo,
        db=db,
    )


@router.get("/me", response_model=UserRead)
async def get_me(
    user: get_current_user,
):
    return user
