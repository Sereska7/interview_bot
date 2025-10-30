from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID as UUIDType

from bot.pkg.models.base_model import Base
from bot.pkg.models.sql_models.question import DifficultyLevel


class ExamResult(Base):
    __tablename__ = "exam_result"

    exam_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("category.category_id", ondelete="SET NULL"),
        nullable=True,
    )

    grade_level: Mapped[DifficultyLevel] = mapped_column(
        Enum(DifficultyLevel, name="exam_grade_level"),
        nullable=False,
    )

    total_questions: Mapped[int] = mapped_column(nullable=False)
    correct_answers: Mapped[int] = mapped_column(nullable=False)
    hints_used: Mapped[int] = mapped_column(default=0, nullable=False)
    score_percent: Mapped[float] = mapped_column(nullable=False)

    started_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    finished_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user = relationship("User", back_populates="exams")
    category = relationship("Category")


