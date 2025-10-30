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
    ) -> list[models.Question] | None:
        """
        Возвращает список вопросов по категории и уровню сложности.
        """
        async with get_connection() as session:
            category_stmt = select(Category.category_id).where(Category.name == cmd.category)
            category_result = await session.execute(category_stmt)
            category_id = category_result.scalar_one_or_none()

            if category_id is None:
                return []

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

            return questions

    @collect_response
    async def get_random_question(
        self,
        exclude_ids: list[int] | None = None
    ) -> models.Question:
        """"""
        async with get_connection() as session:
            stmt = select(Question)

            if exclude_ids:
                stmt = stmt.where(~Question.question_id.in_(exclude_ids))

            stmt = stmt.order_by(func.random()).limit(1)

            result = await session.execute(stmt)
            question = result.scalar_one_or_none()

            if not question:
                fallback_stmt = select(Question).order_by(func.random()).limit(1)
                result = await session.execute(fallback_stmt)
                question = result.scalar_one_or_none()

            return question