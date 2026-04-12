from uuid import UUID

from fastapi import APIRouter

from app.api.dependencies import get_db_dep, note_repository_dep, note_service_dep, place_repository_dep
from app.schemas.note import UpdateNote, NoteCreate, NoteCreateIn

router = APIRouter()


@router.put("/{note_id}")
async def update(
    note_id: UUID,
    db: get_db_dep,
    data: UpdateNote,
    repo: note_repository_dep,
    service: note_service_dep,
):
    return await service.update(data=data, repo=repo, db=db, filters={"id": note_id})

@router.post("/{place_id}/notes")
async def add_note(
    place_id: UUID,
    data: NoteCreateIn,
    db: get_db_dep,
    repo: note_repository_dep,
    place_repo: place_repository_dep,
    service: note_service_dep,
):
    return await service.add_to_place(
        db=db,
        repo=repo,
        place_repo=place_repo,
        place_id=place_id,
        data=data
    )

