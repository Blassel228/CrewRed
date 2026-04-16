from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies import (
    user_service_dep,
    auth_service_dep,
    get_current_user,
    unit_of_work_dep,
)
from app.schemas.user import UserCreateIn, UserUpdateIn, UserRead

router = APIRouter()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreateIn,
    auth_service: auth_service_dep,
    service: user_service_dep,
    unit_of_work: unit_of_work_dep,
):
    return await service.add(
        unit_of_work=unit_of_work,
        data=data,
        auth_service=auth_service,
    )


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    data: UserUpdateIn,
    auth_service: auth_service_dep,
    service: user_service_dep,
    unit_of_work: unit_of_work_dep,
):
    return await service.update(
        unit_of_work=unit_of_work,
        user_id=user_id,
        data=data,
        auth_service=auth_service,
    )


@router.put("/self-update", response_model=UserRead)
async def update_user_self(
    user: get_current_user,
    data: UserUpdateIn,
    auth_service: auth_service_dep,
    service: user_service_dep,
    unit_of_work: unit_of_work_dep,
):
    return await service.update(
        unit_of_work=unit_of_work,
        user_id=user.id,
        data=data,
        auth_service=auth_service,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    service: user_service_dep,
    unit_of_work: unit_of_work_dep,
):
    await service.delete(
        unit_of_work=unit_of_work,
        user_id=user_id,
    )


@router.get("/me", response_model=UserRead)
async def get_me(
    user: get_current_user,
):
    return user
