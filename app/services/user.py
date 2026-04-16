from uuid import UUID

from fastapi import HTTPException

from app.schemas.user import UserCreateIn, UserCreate, UserUpdate, UserUpdateIn
from app.services.auth import AuthService
from app.utils.unit_of_work import UnitOfWork


class UserService:
    async def add(
        self,
        unit_of_work: UnitOfWork,
        data: UserCreateIn,
        auth_service: AuthService,
    ):
        async with unit_of_work:
            existing_user = await unit_of_work.user.get_one_or_none(
                filters={"email": data.email}
            )

        if existing_user:
            raise HTTPException(
                status_code=409, detail="User with such an email already exists."
            )

        hashed_password = auth_service.get_password_hash(data.password)

        payload = UserCreate(
            **data.model_dump(exclude={"password"}), hashed_password=hashed_password
        )
        async with unit_of_work:
            return await unit_of_work.user.add(data=payload)

    async def update(
        self,
        unit_of_work: UnitOfWork,
        user_id: UUID,
        data: UserUpdateIn,
        auth_service: AuthService,
    ):
        async with unit_of_work:
            existing_user = await unit_of_work.user.get_one_or_none(
                filters={"id": user_id}
            )

        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with such an email already exists."
            )

        if data.password:
            hashed_password = auth_service.get_password_hash(data.password)
            payload = UserUpdate(
                **data.model_dump(exclude_none=True, exclude={"password"}),
                hashed_password=hashed_password,
            )
        else:
            payload = UserUpdate(**data.model_dump(exclude_none=True))

        async with unit_of_work:
            return await unit_of_work.user.update(filters={"id": user_id}, data=payload)

    async def delete(
        self,
        unit_of_work: UnitOfWork,
        user_id: UUID,
    ):
        async with unit_of_work:
            return await unit_of_work.user.delete(filters={"id": user_id})
