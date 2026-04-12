from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepository
from app.schemas.user import UserCreateIn, UserCreate, UserUpdate, UserUpdateIn
from app.services.auth import AuthService


class UserService:
    async def add(
        self,
        data: UserCreateIn,
        auth_service: AuthService,
        repo: UserRepository,
        db: AsyncSession,
    ):
        existing_user = await repo.get_one_or_none(db=db, filters={"email": data.email})
        if existing_user:
            raise HTTPException(status_code=409, detail="User with such an email already exists.")
        hashed_password = auth_service.get_password_hash(data.password)
        data = UserCreate(
            **data.model_dump(exclude={"password"}), hashed_password=hashed_password
        )
        return await repo.add(data=data, db=db)

    async def update(
        self,
        user_id: UUID,
        data: UserUpdateIn,
        auth_service: AuthService,
        repo: UserRepository,
        db: AsyncSession,
    ):
        existing_user = await repo.get_one_or_none(db=db, filters={"id": user_id})
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=409, detail="User with such an email already exists.")
        if data.password:
            hashed_password = auth_service.get_password_hash(data.password)
            data = UserUpdate(
                **data.model_dump(exclude_none=True, exclude={"password"}),
                hashed_password=hashed_password,
            )

        return await repo.update(filters={"id": user_id}, data=data, db=db)

    async def delete(self, user_id: UUID, repo: UserRepository, db: AsyncSession):
        return await repo.delete(filters={"id": user_id}, db=db)
