from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.place import PlaceCreateIn


class ProjectCreateIn(BaseModel):
    name: str
    description: str | None = None


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    is_completed: bool = False
    user_id: UUID


class ProjectCreateWithPlacesIn(BaseModel):
    name: str
    description: str | None = None
    is_completed: bool = False
    places: List[PlaceCreateIn] = Field(default_factory=list)


class ProjectUpdate(BaseModel):
    is_completed: bool = False
    name: str | None = None
    description: str | None = None


class ProjectRead(BaseModel):
    id: UUID
    name: str
    is_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
