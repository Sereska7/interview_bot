
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID as UUIDType

from bot.pkg.models.base_model import Base

class UserStatistics(Base):
    __tablename__ = "user_statistics"

    user_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"),
        primary_key=True,
    )

    questions_viewed: Mapped[int] = mapped_column(default=0, nullable=False)
    tests_passed: Mapped[int] = mapped_column(default=0, nullable=False)
    exams_passed: Mapped[int] = mapped_column(default=0, nullable=False)
    favorites_count: Mapped[int] = mapped_column(default=0, nullable=False)

    last_login: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())
    last_test_score: Mapped[Optional[int]] = mapped_column(nullable=True)
    average_exam_score: Mapped[Optional[float]] = mapped_column(nullable=True)

    user = relationship("User", back_populates="statistics", uselist=False)

