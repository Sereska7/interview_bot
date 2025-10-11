"""SQLAlchemy model for users."""

import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType

from sqlalchemy import BigInteger, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.pkg.models.base_model import Base


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=False,
    )

    username: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        index=True,
    )

    first_name: Mapped[Optional[str]] = mapped_column(
        nullable=True,
    )

    registered_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    last_activity: Mapped[Optional[datetime]] = mapped_column(
        onupdate=func.now(),
        nullable=True,
    )

    score: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )

    sessions = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    results = relationship(
        "Result",
        back_populates="user",
        cascade="all, delete-orphan"
    )
