"""Interview question models."""

from datetime import datetime
from uuid import UUID

from bot.pkg.models.sql_models.question import DifficultyLevel
from bot.pkg.models.base import BaseModel


__all__ = [
    "InterviewQuestion",
    "InterviewQuestionReadQuery"
]


class BaseInterviewQuestion(BaseModel):
    """Base model for InterviewQuestion."""


class InterviewQuestion(BaseInterviewQuestion):
    """InterviewQuestion model."""

    kb_question_id: int
    category_id: int
    subtopic: str | None
    title: str
    short_answer: str | None
    detailed_answer: str | None
    examples: str | None
    difficulty: DifficultyLevel
    tags: list[str] | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


#Commands.



#Queries
class InterviewQuestionReadQuery(BaseInterviewQuestion):
    """InterviewQuestionReadQuery model."""

    user_id: UUID
    last_questions: list[int] | None
    difficulty: DifficultyLevel | None
