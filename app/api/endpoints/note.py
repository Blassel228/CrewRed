from uuid import UUID

from fastapi import APIRouter

from app.api.dependencies import (
    unit_of_work_dep,
    note_service_dep,
)
from app.schemas.note import UpdateNote, NoteCreateIn

router = APIRouter()


@router.put("/{note_id}")
async def update(
    note_id: UUID,
    data: UpdateNote,
    unit_of_work: unit_of_work_dep,
    service: note_service_dep,
):
    return await service.update(
        unit_of_work=unit_of_work,
        data=data,
        filters={"id": note_id},
    )


@router.post("/{place_id}/notes")
async def add_note(
    place_id: UUID,
    data: NoteCreateIn,
    unit_of_work: unit_of_work_dep,
    service: note_service_dep,
):
    return await service.add_to_place(
        unit_of_work=unit_of_work,
        place_id=place_id,
        data=data,
    )
