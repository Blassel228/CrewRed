from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.place import PlaceCreate


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    start_date: datetime | None = None


class ProjectCreateWithPlaces(ProjectCreate):
    places: List[PlaceCreate] = Field(default_factory=list)


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: datetime | None = None


class ProjectRead(BaseModel):
    id: UUID
    name: str
    is_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
