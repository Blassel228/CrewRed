from uuid import UUID

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, CreatedAtModel, UUIDModel


class Note(Base, CreatedAtModel, UUIDModel):
    __tablename__ = "notes"

    place_id: Mapped[UUID] = mapped_column(
        ForeignKey("places.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    place: Mapped["Place"] = relationship(back_populates="notes")
