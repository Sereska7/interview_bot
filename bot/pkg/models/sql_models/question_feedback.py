import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Enum, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID as UUIDType

from bot.pkg.models.base_model import Base

class FeedbackMark(str, enum.Enum):
    KNOW = "know"        # ✅ Знаю
    HARD = "hard"        # ⚙️ Сложно
    UNKNOWN = "unknown"  # ❌ Не знаю
    FAVORITE = "favorite"  # ⭐ Избранное


class QuestionFeedback(Base):
    __tablename__ = "question_feedback"

    feedback_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("interview_question.kb_question_id", ondelete="CASCADE"),
        nullable=False,
    )

    mark: Mapped[FeedbackMark] = mapped_column(
        Enum(FeedbackMark, name="feedback_mark"),
        nullable=False,
    )

    comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    user = relationship("User", back_populates="feedbacks")
    question = relationship("InterviewQuestion", back_populates="feedbacks")

