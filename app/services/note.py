from uuid import UUID

from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Note
from app.repositories.note import NoteRepository
from app.repositories.place import PlaceRepository
from app.schemas.note import UpdateNote, NoteCreate, NoteCreateIn


class NoteService:
    async def update(
        self,
        filters: dict[str, any],
        db: AsyncSession,
        data: UpdateNote,
        repo: NoteRepository,
    ) -> Sequence[Note]:
        return await repo.update(db=db, data=data, filters=filters)

    async def add_to_place(
        self,
        db: AsyncSession,
        repo: NoteRepository,
        place_repo: PlaceRepository,
        place_id: UUID,
        data: NoteCreateIn,
    ):
        place = await place_repo.get_one(db, {"id": place_id})

        note = await repo.add(
            db=db,
            data=NoteCreate(
                content=data.content,
                place_id=place.id
            )
        )

        return note
