"""SQLAlchemy model for questions."""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, func, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from bot.pkg.models.base_model import Base


class DifficultyLevel(str, enum.Enum):
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_text: Mapped[str] = mapped_column(nullable=False)
    options: Mapped[dict[str, str]] = mapped_column(JSON, nullable=False)
    correct_option: Mapped[str] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"))
    category_rel = relationship("Category", back_populates="questions")

    difficulty: Mapped[DifficultyLevel] = mapped_column(
        Enum(DifficultyLevel, name="difficultylevel", create_type=True),
        nullable=False
    )
    explanation: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    results = relationship("Result", back_populates="questions", cascade="all, delete-orphan")