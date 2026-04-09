from typing import Any, Optional, Sequence, List
from sqlalchemy import select, update, delete, insert, and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
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
            raise ValueError(f"{self.model.__name__} not found for filters: {filters}")
        return result

    async def get_many(
        self,
        db: AsyncSession,
        filters: Optional[dict[str, Any]] = None,
    ) -> Sequence:
        stmt = select(self.model)

        if filters:
            stmt = stmt.where(and_(*self.build_filters(filters)))

        result = await db.scalars(stmt)
        items = result.all()

        if not items:
            raise NoResultFound(f"{self.model.__name__} not found")

        return items

    async def get_many_or_none(
        self,
        db: AsyncSession,
        filters: Optional[dict[str, Any]] = None,
    ) -> Optional[Sequence]:
        stmt = select(self.model)

        if filters:
            stmt = stmt.where(and_(*self.build_filters(filters)))

        result = await db.scalars(stmt)
        items = result.all()

        return items or None

    async def add(self, db: AsyncSession, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump(exclude_none=True))
        await db.execute(stmt)
        await db.commit()
        return await self.get_one(db, {"id": data.id})

    async def update(self, db: AsyncSession, filters: dict[str, Any], data: BaseModel):
        stmt = update(self.model).values(**data.model_dump(exclude_none=True))
        if filters:
            stmt = stmt.where(and_(*self.build_filters(filters)))
        await db.execute(stmt)
        await db.commit()
        return await self.get_one_or_none(db, filters)

    async def delete(self, db: AsyncSession, filters: dict[str, Any]) -> bool:
        stmt = delete(self.model).where(and_(*self.build_filters(filters)))
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0
