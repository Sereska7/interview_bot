"""SQLAlchemy model for sessions."""

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID as UUIDType

from bot.pkg.models.base_model import Base


class Session(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUIDType] = mapped_column(ForeignKey("user.user_id", ondelete="CASCADE"))
    category: Mapped[str] = mapped_column(String(100), nullable=True)

    started_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    finished_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    score: Mapped[Optional[int]] = mapped_column(default=0)

    user = relationship("User", back_populates="sessions")
    results = relationship("Result", back_populates="sessions", cascade="all, delete-orphan")
