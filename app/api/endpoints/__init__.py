from fastapi import APIRouter

from app.api.endpoints import artWork
from app.api.endpoints import auth
from app.api.endpoints import note
from app.api.endpoints import place
from app.api.endpoints import project
from app.api.endpoints import user

api_router = APIRouter(prefix="/api")

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(project.router, prefix="/project", tags=["Project"])
api_router.include_router(note.router, prefix="/note", tags=["Note"])
api_router.include_router(place.router, prefix="/place", tags=["Place"])
api_router.include_router(artWork.router, prefix="/artWork", tags=["ArtWork"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
