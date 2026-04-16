from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import session as async_session
from app.repositories.note import NoteRepository
from app.repositories.place import PlaceRepository
from app.repositories.project import ProjectRepository
from app.repositories.user import UserRepository


class AbstractUnitOfWork(ABC):
    session: AsyncSession

    project: ProjectRepository
    place: PlaceRepository
    note: NoteRepository
    user: UserRepository

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        pass


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.session_factory = async_session

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self.session_factory()

        self.user = UserRepository(self.session)
        self.project = ProjectRepository(self.session)
        self.note = NoteRepository(self.session)
        self.place = PlaceRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.session.rollback()
        else:
            await self.session.commit()

        await self.session.close()

