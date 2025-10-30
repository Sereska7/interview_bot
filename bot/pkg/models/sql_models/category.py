"""SQLAlchemy model for categories."""

from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.pkg.models.base_model import Base


class Category(Base):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    questions = relationship("Question", back_populates="category_rel", cascade="all, delete-orphan")
    kb_questions = relationship("InterviewQuestion", back_populates="category", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="category")
