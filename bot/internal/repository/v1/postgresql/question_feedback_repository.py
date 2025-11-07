from sqlalchemy import func
from sqlalchemy.sql.expression import select

from bot.internal.repository.repository import Repository
from bot.internal.repository.v1.postgresql.connection import get_connection
from bot.internal.repository.v1.postgresql.handlers.collect_response import collect_response
from bot.pkg.models.sql_models import QuestionFeedback
from bot.pkg.models import v1 as models


class QuestionFeedbackRepository(Repository):
    """"""

    @collect_response
    async def create_feedback(
        self,
        cmd: models.QuestionFeedbackCreateCommand
    ) -> models.QuestionFeedback:
        async with get_connection() as session:
            existing_feedback = await session.execute(
                select(QuestionFeedback)
                .where(
                    QuestionFeedback.user_id == cmd.user_id,
                    QuestionFeedback.question_id == cmd.question_id
                )
            )
            feedback = existing_feedback.scalar_one_or_none()

            if feedback:
                feedback.mark = cmd.mark
                feedback.updated_at = func.now()
            else:
                feedback = QuestionFeedback(
                    user_id=cmd.user_id,
                    question_id=cmd.question_id,
                    mark=cmd.mark
                )
                session.add(feedback)

            await session.commit()
            await session.refresh(feedback)
            return feedback

    @collect_response
    async def read_by_user_and_question(
            self, user_id: int, question_id: int
    ) -> QuestionFeedback | None:
        """Возвращает фидбек пользователя по конкретному вопросу (если есть)."""

        async with get_connection() as session:
            stmt = select(QuestionFeedback).where(
                QuestionFeedback.user_id == user_id,
                QuestionFeedback.question_id == question_id,
            )
            result = await session.execute(stmt)
            feedback = result.scalar_one_or_none()
            return feedback


