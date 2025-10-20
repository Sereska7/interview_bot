"""User models."""

from datetime import datetime
from uuid import UUID

from bot.pkg.models.base import BaseModel


__all__ = [
    "User",
    "CreateUser"
]


class BaseUser(BaseModel):
    """Base model for User."""


class User(BaseUser):
    """User model."""

    user_id: UUID
    telegram_id: int
    username: str
    first_name: str
    registered_at: datetime
    last_activity: datetime | None
    score: int


class CreateUser(BaseUser):
    """Create User model."""

    telegram_id: int
    username: str
    first_name: str
