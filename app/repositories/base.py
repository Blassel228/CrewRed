from typing import Any, List

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, update, delete, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class BaseRepository:
    model = None
    session: AsyncSession | None = None
    eager_load: list | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    def build_filters(self, filters: dict[str, Any]) -> List:
        conditions = []
        for attr, value in filters.items():
            if hasattr(self.model, attr):
                column = getattr(self.model, attr)
                if isinstance(value, list):
                    conditions.append(column.in_(value))
                else:
                    conditions.append(column == value)
        return conditions

    def apply_eager_load(self, stmt):
        if self.eager_load:
            for relation in self.eager_load:
                stmt = stmt.options(selectinload(relation))
        return stmt

    async def get_one_or_none(self, filters: dict[str, any]):
        stmt = select(self.model).where(and_(*self.build_filters(filters)))
        stmt = self.apply_eager_load(stmt)
        return await self.session.scalar(stmt)

    async def get_one(self, filters: dict[str, any]):
        result = await self.get_one_or_none(filters)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found for filters: {filters}",
            )
        return result

    async def get_many(self, filters=None, limit=None, offset=None):
        stmt = select(self.model)

        if filters:
            stmt = stmt.where(and_(*self.build_filters(filters)))

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        stmt = self.apply_eager_load(stmt)

        result = await self.session.scalars(stmt)
        items = result.all()

        if not items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )

        return items

    async def get_many_or_none(self, filters=None, limit=None, offset=None):
        stmt = select(self.model)

        if filters:
            stmt = stmt.where(and_(*self.build_filters(filters)))

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        stmt = self.apply_eager_load(stmt)

        result = await self.session.scalars(stmt)
        items = result.all()

        return items or None

    async def add(self, data: BaseModel):
        stmt = (
            insert(self.model)
            .values(**data.model_dump(exclude_none=True))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update(self, filters: dict[str, Any], data: BaseModel):
        stmt = update(self.model).values(**data.model_dump(exclude_none=True))

        if filters:
            stmt = stmt.where(and_(*self.build_filters(filters)))

        await self.session.execute(stmt)

        stmt = select(self.model).where(and_(*self.build_filters(filters)))
        stmt = self.apply_eager_load(stmt)

        updated = await self.session.scalar(stmt)
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found for update",
            )

        return updated

    async def delete(self, filters: dict[str, Any]) -> bool:
        stmt = delete(self.model).where(and_(*self.build_filters(filters)))
        result = await self.session.execute(stmt)
        return result.rowcount > 0
