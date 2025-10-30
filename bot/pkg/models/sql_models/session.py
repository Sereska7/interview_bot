"""SQLAlchemy model for sessions."""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID as UUIDType

from bot.pkg.models.base_model import Base
from bot.pkg.models.sql_models.question import DifficultyLevel


class SessionType(str, enum.Enum):
    TEST = "test"
    EXAM = "exam"
    RANDOM = "random"


class Session(Base):
    __tablename__ = "session"

    session_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUIDType] = mapped_column(ForeignKey("user.user_id", ondelete="CASCADE"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.category_id", ondelete="SET NULL"))



    grade_level: Mapped[Optional[DifficultyLevel]] = mapped_column(
        Enum(DifficultyLevel, name="session_grade_level"),
        nullable=True,
    )

    total_questions: Mapped[Optional[int]] = mapped_column(nullable=True)
    correct_answers: Mapped[Optional[int]] = mapped_column(nullable=True)
    score_percent: Mapped[Optional[float]] = mapped_column(nullable=True)

    started_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    finished_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    score: Mapped[Optional[int]] = mapped_column(default=0)

    user = relationship("User", back_populates="sessions")
    results = relationship("Result", back_populates="session", cascade="all, delete-orphan")
    category = relationship("Category", back_populates="sessions")

