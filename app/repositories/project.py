from app.db.models.project import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository):
    model = Project
