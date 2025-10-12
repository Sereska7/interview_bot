

__all__ = [
    "Question",
    "QuestionReadCommand"
]

from bot.pkg.models.base import BaseModel


class BaseQuestion(BaseModel):
    """Base question model."""


class Question(BaseQuestion):
    """Question model."""


class QuestionReadCommand(BaseQuestion):
    """Question read command."""

    category: str
    difficulty: str
    limit: int = 10
