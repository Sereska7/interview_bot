import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Enum, func, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID as UUIDType

from bot.pkg.models.base_model import Base
from bot.pkg.models.sql_models.question import DifficultyLevel


class UserProfile(Base):
    __tablename__ = "user_profile"

    user_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"),
        primary_key=True,
    )

    current_grade: Mapped[Optional[DifficultyLevel]] = mapped_column(
        Enum(DifficultyLevel, name="user_grade_level"),
        nullable=True,
    )

    target_grade: Mapped[Optional[DifficultyLevel]] = mapped_column(
        Enum(DifficultyLevel, name="user_target_grade_level"),
        nullable=True,
    )

    language: Mapped[str] = mapped_column(String(5), default="ru", nullable=False)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    user = relationship("User", back_populates="profile", uselist=False)

