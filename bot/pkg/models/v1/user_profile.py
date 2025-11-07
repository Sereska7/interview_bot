"""User models."""

from datetime import datetime
from uuid import UUID

from bot.pkg.models.sql_models.question import DifficultyLevel
from bot.pkg.models.base import BaseModel


__all__ = [
    "UserProfile",
    "UserProfileCreateCommand"
]


class BaseUserProfile(BaseModel):
    """Base model for User profile."""


class UserProfile(BaseUserProfile):
    """UserProfile model."""

    user_id: UUID
    current_grade: DifficultyLevel | None
    target_grade: DifficultyLevel | None
    language: str
    notifications_enabled: bool
    timezone: str
    created_at: datetime
    updated_at: datetime



#Commands
class UserProfileCreateCommand(BaseUserProfile):
    """"""

    user_id: UUID
