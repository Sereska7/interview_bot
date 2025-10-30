import random

from aiogram.fsm.context import FSMContext

from bot.internal.repository.v1.postgresql.question import QuestionRepository
from bot.pkg.models import v1 as models
from bot.pkg.models.sql_models.question import DifficultyLevel
from bot.utils import save_message_id
from bot.utils.constants import escape_md


class QuestionService:
    """Question services class."""

    question_repository: QuestionRepository

    async def get_questions(
        self,
        cmd: models.QuestionReadCommand
    ) -> list[models.Question] | None:
        """"""

        questions = await self.question_repository.read_questions_by_filters(cmd)

        for question in questions:
            options = question.options
            correct_key = question.correct_option
            correct_value = options[correct_key]

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

    async def get_questions_or_alert(
        self,
        category: str,
        level: str,
        chat_id: int,
        state: FSMContext,
        bot
    ) -> list[models.Question] | None:
        cmd = models.QuestionReadCommand(
            category=category.capitalize(),
            difficulty=DifficultyLevel[level.upper()],
            limit=10
        )
        questions = await self.get_questions(cmd)
        if not questions:
            msg = await bot.send_message(
                chat_id=chat_id,
                text="❌ К сожалению, вопросы для этой темы/уровня не найдены.",
                parse_mode="HTML"
            )
            await save_message_id(state, msg.message_id)
            return []
        return questions

    async def get_random_question(
        self,
        exclude_ids: list[int] | None = None
    ) -> models.Question:
        """"""

        question = await self.question_repository.get_random_question(exclude_ids)

        if question.options:
            options = question.options
            correct_key = question.correct_option
            correct_value = options[correct_key]

            keys = list(options.keys())
            values = list(options.values())

            random.shuffle(values)
            new_options = dict(zip(keys, values))
            question.options = new_options

            for key, value in new_options.items():
                if value == correct_value:
                    question.correct_option = key
                    break

        return question



