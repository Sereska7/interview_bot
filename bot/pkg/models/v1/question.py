from datetime import datetime

from bot.pkg.models.base import BaseModel
from bot.pkg.models.sql_models.question import DifficultyLevel

__all__ = [
    "Question",
    "QuestionReadCommand",
    "QuestionResponse"
]


class BaseQuestion(BaseModel):
    """Base question model."""


class Question(BaseModel):
    id: int
    question_text: str
    options: dict[str, str]
    correct_option: str
    category_id: int
    difficulty: DifficultyLevel
    explanation: str | None = None
    created_at: datetime


class QuestionResponse(BaseModel):
    id: int
    options: dict[str, str]
    question_text: str
    correct_option: str
    explanation: str


class QuestionReadCommand(BaseQuestion):
    """Question read command."""

    category: str
    difficulty: DifficultyLevel
    limit: int = 10
