from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.project import ProjectRepository
from app.repositories.place import PlaceRepository
from app.repositories.note import NoteRepository
from app.repositories.user import UserRepository
from app.schemas.auth import TokenData
from app.services.artworkApi import ArtworkApiService
from app.services.auth import auth_service, AuthService
from app.services.project import ProjectService
from app.services.note import NoteService
from app.services.place import PlaceService
from app.services.user import UserService
from app.utils.deps import get_db

get_db_dep = Annotated[AsyncSession, Depends(get_db)]

get_current_user = Annotated[TokenData, Depends(auth_service.get_current_user)]

project_repository_dep = Annotated[ProjectRepository, Depends(ProjectRepository)]
note_repository_dep = Annotated[NoteRepository, Depends(NoteRepository)]
place_repository_dep = Annotated[PlaceRepository, Depends(PlaceRepository)]
user_repository_dep = Annotated[UserRepository, Depends(UserRepository)]

project_service_dep = Annotated[ProjectService, Depends(ProjectService)]
note_service_dep = Annotated[NoteService, Depends(NoteService)]
place_service_dep = Annotated[PlaceService, Depends(PlaceService)]
user_service_dep = Annotated[UserService, Depends(UserService)]
art_work_dep = Annotated[ArtworkApiService, Depends(ArtworkApiService)]
auth_service_dep = Annotated[AuthService, Depends(AuthService)]
