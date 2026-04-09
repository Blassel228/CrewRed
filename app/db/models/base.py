from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class UUIDModel:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)


class CreatedAtModel:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )


class Base(DeclarativeBase):
    type_annotation_map = {
        UUID: postgresql.UUID,
        dict[str, Any]: postgresql.JSON,
        list[dict[str, Any]]: postgresql.ARRAY(postgresql.JSON),
        list[str]: postgresql.ARRAY(String),
        Decimal: postgresql.NUMERIC(10, 2),
        datetime: DateTime(timezone=True),
        bool: Boolean,
    }
