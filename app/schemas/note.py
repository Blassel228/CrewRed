from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NoteCreate(BaseModel):
    content: str


class UpdateNote(BaseModel):
    content: str


class NoteRead(BaseModel):
    id: UUID
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
