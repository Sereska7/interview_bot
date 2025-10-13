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

        for question in questions:
            options = question.options
            correct_key = question.correct_option
            correct_value = options[correct_key]

            # Разделяем ключи и значения
            keys = list(options.keys())
            values = list(options.values())

            random.shuffle(values)

            new_options = dict(zip(keys, values))
            question.options = new_options

            for key, value in new_options.items():
                if value == correct_value:
                    question.correct_option = key
                    break

        return questions



