from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Enum, func, String, Text, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.pkg.models.base_model import Base
from bot.pkg.models.sql_models.question import DifficultyLevel

class InterviewQuestion(Base):
    __tablename__ = "interview_question"

    kb_question_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.category_id", ondelete="CASCADE"),
        nullable=False,
    )

    subtopic: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    short_answer: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    detailed_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    examples: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    difficulty: Mapped[DifficultyLevel] = mapped_column(
        Enum(DifficultyLevel, name="kb_difficulty"),
        nullable=False,
    )

    tags: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    category = relationship("Category", back_populates="kb_questions")
    feedbacks = relationship(
        "QuestionFeedback",
        back_populates="question",
        cascade="all, delete-orphan"
    )

