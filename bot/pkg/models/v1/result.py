"""Result models."""

from datetime import datetime
from uuid import UUID

from bot.pkg.models.base import BaseModel


__all__ = [
    "Result",
    "ResultCreateCommand",
    "ResultResponse"
]

from bot.pkg.models.v1 import QuestionResponse


class BaseResult(BaseModel):
    """Base model for Result."""


class Result(BaseResult):

    result_id: int
    user_id: UUID
    question_id: int
    session_id: int | None
    chosen_option: str
    is_correct: bool
    answered_at: datetime


class ResultResponse(BaseResult):

    result_id: int
    user_id: UUID
    question_id: int
    session_id: int
    chosen_option: str
    is_correct: bool
    answered_at: datetime
    question: QuestionResponse


class ResultCreateCommand(BaseResult):

    user_id: UUID
    session_id: int | None
    question_id: int
    chosen_option: str
    is_correct: bool
