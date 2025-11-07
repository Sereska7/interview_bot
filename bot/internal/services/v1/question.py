import random

from aiogram.fsm.context import FSMContext

from bot.internal.repository.v1.postgresql.question import QuestionRepository
from bot.pkg.keyboards.test import empty_questions_kb
from bot.pkg.models import v1 as models
from bot.pkg.models.sql_models.question import DifficultyLevel
from bot.pkg.states.test_state import TestStates
from bot.utils import save_message_id


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
        callback
    ) -> list[models.Question] | None:
        cmd = models.QuestionReadCommand(
            category=category.capitalize(),
            difficulty=DifficultyLevel[level.upper()],
            limit=10
        )
        questions = await self.get_questions(cmd)
        if not questions:
            await state.set_state(TestStates.select_topic)
            msg = await callback.message.edit_text(
                text=(
                    f"❌ Вопросы не найдены.\n\n"
                    f"✅ Тема: *{category}*\n"
                    f"⚡ Уровень: *{level.capitalize()}*\n\n"
                    "Попробуйте выбрать другую тему или уровень сложности 👇"
                ),
                reply_markup=empty_questions_kb,
                parse_mode="Markdown"
            )
            await save_message_id(state, msg.message_id)
            return []
        return questions
