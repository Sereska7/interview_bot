from uuid import UUID

from sqlalchemy import func
from sqlalchemy.sql.expression import select

from bot.internal.repository.repository import Repository
from bot.internal.repository.v1.postgresql.connection import get_connection
from bot.internal.repository.v1.postgresql.handlers.collect_response import collect_response
from bot.pkg.models.sql_models import InterviewQuestion, QuestionFeedback, Category
from bot.pkg.models import v1 as models
from bot.pkg.models.sql_models.question import DifficultyLevel
from bot.pkg.models.sql_models.question_feedback import FeedbackMark


class InterviewQuestionRepository(Repository):
    """Interview repository implementation."""

    @collect_response
    async def read_question_by_filters(
        self,
        query: models.InterviewQuestionReadQuery
    ) -> tuple[models.InterviewQuestion, models.QuestionFeedback | None]:
        """Получить случайный вопрос по сложности, исключая уже показанные, вместе с оценкой пользователя."""

        async with get_connection() as session:
            stmt = select(InterviewQuestion).where(
                InterviewQuestion.is_active.is_(True)
            )

            if query.difficulty is not None:
                difficulty = query.difficulty
                if isinstance(difficulty, str):
                    difficulty = DifficultyLevel[difficulty.upper()]
                stmt = stmt.where(InterviewQuestion.difficulty == difficulty)

            exclude_ids = [i for i in (query.last_questions or []) if i]
            if exclude_ids:
                stmt = stmt.where(~InterviewQuestion.kb_question_id.in_(exclude_ids))

            stmt = stmt.order_by(func.random()).limit(1)
            result = await session.execute(stmt)
            question = result.scalar_one_or_none()

            if not question:
                fallback_stmt = select(InterviewQuestion).where(
                    InterviewQuestion.is_active.is_(True)
                ).order_by(func.random()).limit(1)
                result = await session.execute(fallback_stmt)
                question = result.scalar_one_or_none()

            feedback = None
            if query.user_id:
                feedback_result = await session.execute(
                    select(QuestionFeedback)
                    .where(
                        QuestionFeedback.user_id == query.user_id,
                        QuestionFeedback.question_id == question.kb_question_id,
                    )
                )
                feedback = feedback_result.scalar_one_or_none()

            return question, feedback

    @collect_response
    async def read_unknown_question(
        self,
        user_id: int,
        last_questions: list[int] | None = None
    ) -> tuple[models.InterviewQuestion | None, models.QuestionFeedback | None]:
        """Возвращает случайный вопрос, который пользователь отметил как 'не знаю', вместе с фидбеком."""

        async with get_connection() as session:
            stmt = (
                select(InterviewQuestion, QuestionFeedback)
                .join(QuestionFeedback, QuestionFeedback.question_id == InterviewQuestion.kb_question_id)
                .where(
                    QuestionFeedback.user_id == user_id,
                    QuestionFeedback.mark == FeedbackMark.UNKNOWN,
                    InterviewQuestion.is_active.is_(True)
                )
            )

            if last_questions:
                stmt = stmt.where(~InterviewQuestion.kb_question_id.in_(last_questions))

            stmt = stmt.order_by(func.random()).limit(1)

            result = await session.execute(stmt)
            row = result.first()

            if not row:
                return None, None

            question, feedback = row
            return question, feedback

    @collect_response
    async def get_interview_questions(
        self,
        topic: str,
        level: str,
        user_id: int | None = None,
    ) -> list[models.InterviewQuestion] | None:
        """
        Получить список случайных активных вопросов по теме и уровню сложности
        вместе с пользовательским feedback (если есть).

        Args:
            topic (str): Название темы (например, "Python").
            level (str): Уровень сложности ("Junior", "Middle", "Senior").
            user_id (int | None): ID пользователя (для получения feedback).

        Returns:
            tuple[list[InterviewQuestion], list[QuestionFeedback | None]]
        """

        async with get_connection() as session:
            # 🔹 Базовый запрос: активные вопросы по теме
            stmt = select(InterviewQuestion).where(
                InterviewQuestion.is_active.is_(True)
            )

            # 🔹 Фильтр по теме
            subquery = select(Category.category_id).where(Category.name == topic)
            stmt = stmt.where(InterviewQuestion.category_id.in_(subquery))

            # 🔹 Фильтр по уровню сложности
            try:
                difficulty_enum = DifficultyLevel[level.upper()]
                stmt = stmt.where(InterviewQuestion.difficulty == difficulty_enum)
            except KeyError:
                pass

            # 🔹 Случайная выборка (до 15 вопросов)
            stmt = stmt.order_by(func.random()).limit(15)
            result = await session.execute(stmt)
            questions = result.scalars().all()

            # 🔸 fallback — если недостаточно вопросов
            if not questions or len(questions) < 15:
                fallback_stmt = (
                    select(InterviewQuestion)
                    .where(InterviewQuestion.is_active.is_(True))
                    .order_by(func.random())
                    .limit(15)
                )
                result = await session.execute(fallback_stmt)
                questions = result.scalars().all()

            return questions

    @collect_response
    async def get_feedback_question(
        self,
        user_id: UUID,
        question_id: int
    ) -> models.QuestionFeedback | None:
        """"""

        async with get_connection() as session:
            stmt = select(QuestionFeedback).where(
                QuestionFeedback.question_id == question_id,
                QuestionFeedback.user_id == user_id
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
