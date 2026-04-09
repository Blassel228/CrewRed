from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.project import ProjectRepository
from app.repositories.place import PlaceRepository
from app.repositories.note import NoteRepository
from app.services.artworkApi import ArtworkApiService
from app.services.project import ProjectService
from app.services.note import NoteService
from app.services.place import PlaceService
from app.utils.deps import get_db

get_db_dep = Annotated[AsyncSession, Depends(get_db)]

project_repository_dep = Annotated[ProjectRepository, Depends(ProjectRepository)]
note_repository_dep = Annotated[NoteRepository, Depends(NoteRepository)]
place_repository_dep = Annotated[PlaceRepository, Depends(PlaceRepository)]

project_service_dep = Annotated[ProjectService, Depends(ProjectService)]
note_service_dep = Annotated[NoteService, Depends(NoteService)]
place_service_dep = Annotated[PlaceService, Depends(PlaceService)]
art_work_dep = Annotated[ArtworkApiService, Depends(ArtworkApiService)]
