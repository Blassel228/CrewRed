from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from app.schemas.note import NoteRead


class PlaceCreateIn(BaseModel):
    external_id: str
    name: str
    longitude: Optional[float] = None
    latitude: Optional[float] = None


class PlaceCreate(PlaceCreateIn):
    project_id: UUID


class PlaceVisitedUpdate(BaseModel):
    is_visited: Optional[bool] = None


class PlaceRead(BaseModel):
    id: UUID
    external_id: str
    name: str
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    is_visited: bool
    created_at: datetime

    class Config:
        from_attributes = True
