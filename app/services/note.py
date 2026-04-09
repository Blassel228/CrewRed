from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.note import NoteRepository
from app.schemas.note import UpdateNote


class NoteService:
    async def update_note(
        self, db: AsyncSession, data: UpdateNote, repo: NoteRepository
    ):
        return await repo.update(db=db, data=data, filters=data.model_dump())
