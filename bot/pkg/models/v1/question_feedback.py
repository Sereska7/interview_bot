"""Question feedback models."""

from datetime import datetime
from uuid import UUID

from bot.pkg.models.base import BaseModel


__all__ = [
    "QuestionFeedback",
    "QuestionFeedbackCreateCommand"
]

from bot.pkg.models.sql_models.question_feedback import FeedbackMark


class BaseQuestionFeedback(BaseModel):
    """Base model for QuestionFeedback."""


class QuestionFeedback(BaseQuestionFeedback):
    """"""

    feedback_id: int
    user_id: UUID
    question_id: int
    mark: FeedbackMark
    comment: str | None
    updated_at: datetime


#Command.
class QuestionFeedbackCreateCommand(BaseQuestionFeedback):
    """"""

    user_id: UUID
    question_id: int
    mark: FeedbackMark
