import random

from bot.internal.repository.v1.postgresql.question import QuestionRepository
from bot.pkg.models import v1 as models


class QuestionService:
    """Question services class."""

    question_repository: QuestionRepository

    async def get_questions(
        self,
        cmd: models.QuestionReadCommand
    ):
        """"""

        questions = await self.question_repository.read_questions_by_filters(cmd)

        random.shuffle(questions)

        return questions



