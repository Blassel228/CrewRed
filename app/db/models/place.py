from typing import List
from uuid import UUID

from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, CreatedAtModel, UUIDModel


class Place(Base, CreatedAtModel, UUIDModel):
    __tablename__ = "places"

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    external_id: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)

    is_visited: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    project: Mapped["Project"] = relationship(back_populates="places")

    notes: Mapped[List["Note"]] = relationship(
        back_populates="place",
        cascade="all, delete-orphan",
    )
