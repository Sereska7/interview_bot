from datetime import datetime
from uuid import UUID

from bot.pkg.models.base import BaseModel


__all__ = [
    "Session",
    "SessionCreateCommand",
    "SessionUpdateCommand"
]


class BasesSession(BaseModel):
    """"""


class Session(BasesSession):

    session_id: int
    user_id: UUID
    category_id: int | None
    started_at: datetime
    finished_at: datetime | None
    score: int | None


class SessionCreateCommand(BasesSession):

    user_id: UUID
    category: str


class SessionUpdateCommand(BasesSession):

    session_id: int
    score: int | None