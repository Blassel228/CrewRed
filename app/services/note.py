from uuid import UUID

from sqlalchemy import Sequence

from app.db.models import Note
from app.schemas.note import UpdateNote, NoteCreate, NoteCreateIn
from app.utils.unit_of_work import UnitOfWork


class NoteService:
    async def update(
        self,
        unit_of_work: UnitOfWork,
        filters: dict[str, any],
        data: UpdateNote,
    ) -> Sequence[Note]:
        async with unit_of_work:
            return await unit_of_work.note.update(filters=filters, data=data)

    async def add_to_place(
        self,
        unit_of_work: UnitOfWork,
        place_id: UUID,
        data: NoteCreateIn,
    ) -> Note:
        async with unit_of_work:
            place = await unit_of_work.place.get_one({"id": place_id})

            note = await unit_of_work.note.add(
                NoteCreate(content=data.content, place_id=place.id)
            )

            return note
