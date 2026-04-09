from fastapi import APIRouter

from app.api.dependencies import get_db_dep, note_repository_dep, note_service_dep
from app.schemas.note import UpdateNote

router = APIRouter()


@router.put("/")
async def update(
    db: get_db_dep,
    data: UpdateNote,
    repo: note_repository_dep,
    service: note_service_dep,
):
    return await service.update_note(data=data, repo=repo, db=db)
