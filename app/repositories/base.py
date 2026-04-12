from typing import Any, Optional, Sequence, List
from sqlalchemy import select, update, delete, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from pydantic import BaseModel


class BaseRepository:
    model = None

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

    async def get_one_or_none(
        self, db: AsyncSession, filters: dict[str, Any]
    ) -> Optional:
        stmt = select(self.model).where(and_(*self.build_filters(filters)))
        return await db.scalar(stmt)

    async def get_one(self, db: AsyncSession, filters: dict[str, Any]):
        result = await self.get_one_or_none(db, filters)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found for filters: {filters}",
            )
        return result

    async def get_many(
        self,
        db: AsyncSession,
        filters: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Sequence:
        stmt = select(self.model)

        if filters:
            stmt = stmt.where(and_(*self.build_filters(filters)))

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        result = await db.scalars(stmt)
        items = result.all()

        if not items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )

        return items

    async def get_many_or_none(
        self,
        db: AsyncSession,
        filters: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Optional[Sequence]:
        stmt = select(self.model)

        if filters:
            stmt = stmt.where(and_(*self.build_filters(filters)))

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        result = await db.scalars(stmt)
        items = result.all()

        return items or None

    async def add(self, db: AsyncSession, data: BaseModel):
        stmt = (
            insert(self.model)
            .values(**data.model_dump(exclude_none=True))
            .returning(self.model)
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    async def update(self, db: AsyncSession, filters: dict[str, Any], data: BaseModel):
        stmt = update(self.model).values(**data.model_dump(exclude_none=True))

        if filters:
            stmt = stmt.where(and_(*self.build_filters(filters)))

        await db.execute(stmt)

        updated = await db.scalar(
            select(self.model).where(and_(*self.build_filters(filters)))
        )
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found for update",
            )

        return updated

    async def delete(self, db: AsyncSession, filters: dict[str, Any]) -> bool:
        stmt = delete(self.model).where(and_(*self.build_filters(filters)))
        result = await db.execute(stmt)
        return result.rowcount > 0
