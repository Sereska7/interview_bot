from sqlalchemy import func
from sqlalchemy.sql.expression import select

from bot.internal.repository.repository import Repository
from bot.internal.repository.v1.postgresql.connection import get_connection
from bot.internal.repository.v1.postgresql.handlers.collect_response import collect_response
from bot.pkg.models.sql_models import Question, Category
from bot.pkg.models import v1 as models


class QuestionRepository(Repository):
    """Question repository implementation."""

    @collect_response
    async def read_questions_by_filters(
        self,
        cmd: models.QuestionReadCommand
    ) -> list[models.Question]:
        """
        Возвращает список вопросов по категории и уровню сложности.
        """
        async with get_connection() as session:
            # Получаем id категории по имени
            category_stmt = select(Category.id).where(Category.name == cmd.category)
            category_result = await session.execute(category_stmt)
            category_id = category_result.scalar_one_or_none()

            if category_id is None:
                # Если такой категории нет, возвращаем пустой список
                return []

            # Теперь достаем вопросы по id категории
            stmt = (
                select(Question)
                .where(
                    Question.category_id == category_id,
                    Question.difficulty == cmd.difficulty
                )
                .order_by(func.random())
                .limit(cmd.limit)
            )
            result = await session.execute(stmt)
            questions = result.scalars().all()

            # Преобразуем в Pydantic модели
            questions_models: list[models.Question] = [
                models.Question.model_validate(q) for q in questions
            ]
            return questions_models
