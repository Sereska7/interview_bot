from sqlalchemy.sql.expression import select

from bot.internal.repository.repository import Repository
from bot.internal.repository.v1.postgresql.connection import get_connection
from bot.internal.repository.v1.postgresql.handlers.collect_response import collect_response
from bot.pkg.models import v1 as models
from bot.pkg.models.sql_models import Result, Question


class ResultRepository(Repository):

    @collect_response
    async def create_result(
        self,
        cmd: models.ResultCreateCommand,
    ) -> models.Result:
        async with get_connection() as session:
            new_result = Result(
                user_id=cmd.user_id,
                question_id=cmd.question_id,
                session_id=cmd.session_id,
                chosen_option=cmd.chosen_option,
                is_correct=cmd.is_correct,
            )

            session.add(new_result)
            await session.commit()
            await session.refresh(new_result)

            return new_result

    @collect_response
    async def get_results_by_session(
        self,
        session_id: int
    ) -> list[models.ResultResponse]:
        async with get_connection() as session:
            results = await session.execute(
                select(Result, Question)
                .join(Question, Result.question_id == Question.question_id)
                .where(Result.session_id == session_id)
            )
            rows = results.all()

            return [
                models.ResultResponse(
                    result_id=r.result_id,
                    user_id=r.user_id,
                    question_id=r.question_id,
                    session_id=r.session_id,
                    chosen_option=r.chosen_option,
                    is_correct=r.is_correct,
                    answered_at=r.answered_at,
                    question=models.QuestionResponse(
                        question_id=q.question_id,
                        options=q.options,
                        question_text=q.question_text,
                        correct_option=q.correct_option,
                        explanation=q.explanation
                    )
                )
                for r, q in rows
            ]