"""SQLAlchemy model for results."""

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID as UUIDType

from bot.pkg.models.base_model import Base


class Result(Base):
    __tablename__ = "result"

    result_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUIDType] = mapped_column(ForeignKey("user.user_id", ondelete="CASCADE"))
    question_id: Mapped[int] = mapped_column(ForeignKey("question.question_id", ondelete="CASCADE"))
    session_id: Mapped[Optional[int]] = mapped_column(ForeignKey("session.session_id", ondelete="CASCADE"), nullable=True)

    chosen_option: Mapped[str] = mapped_column(String, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    answered_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="results")
    session = relationship("Session", back_populates="results")
    question = relationship("Question", back_populates="results")
