from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from app.schemas.note import NoteRead


class PlaceCreate(BaseModel):
    external_id: str
    name: str
    project_id: UUID
    location: Optional[str] = None


class PlaceVisitedUpdate(BaseModel):
    is_visited: Optional[bool] = None


class PlaceRead(BaseModel):
    id: UUID
    external_id: str
    name: str
    location: Optional[str] = None
    is_visited: bool
    created_at: datetime
    notes: list[NoteRead] = []

    class Config:
        from_attributes = True
