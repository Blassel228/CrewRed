from typing import List
from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, CreatedAtModel, UUIDModel


class Project(Base, CreatedAtModel, UUIDModel):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String, nullable=False)

    is_completed: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    places: Mapped[List["Place"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship(back_populates="projects")
