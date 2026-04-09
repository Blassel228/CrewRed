# from typing import List
# from sqlalchemy import String
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from app.db.models.base import Base, CreatedAtModel, UUIDModel
#
#
# class User(Base, CreatedAtModel, UUIDModel):
#     __tablename__ = "users"
#
#     email: Mapped[str] = mapped_column(
#         String(255), unique=True, nullable=False, index=True
#     )
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     surname: Mapped[str] = mapped_column(String(255), nullable=False)
#     password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
#
#     projects: Mapped[List["Project"]] = relationship(
#         back_populates="user",
#         cascade="all, delete-orphan",
#         lazy="selectin",
#     )
#
#     def __repr__(self) -> str:
#         return f"<User(id={self.id}, email='{self.email}')>"
