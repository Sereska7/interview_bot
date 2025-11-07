from uuid import UUID

from bot.internal.repository.v1.postgresql import InterviewQuestionRepository
from bot.pkg.models import v1 as models


class InterviewQuestionService:
    """Interview services class."""

    interview_question_repository: InterviewQuestionRepository

    async def get_random_question(
        self,
        query: models.InterviewQuestionReadQuery
    ) -> tuple[models.InterviewQuestion, models.QuestionFeedback | None]:
        """"""

        question, feedback = await self.interview_question_repository.read_question_by_filters(query)
        return question, feedback

    async def get_unknown_question(
        self,
        user_id: int,
        last_questions: list[int] | None = None
    ) -> tuple[models.InterviewQuestion | None, models.QuestionFeedback | None]:
        """Получает случайный вопрос, ранее отмеченный как 'не знаю'."""

        question, feedback = await self.interview_question_repository.read_unknown_question(user_id, last_questions)
        if not question:
            return None, None


        return question, feedback

    async def get_interview_question(
        self,
        topic,
        level,
        user_id
    ) -> list[models.InterviewQuestion] | None:
        """"""

        questions = await self.interview_question_repository.get_interview_questions(
            topic,
            level,
            user_id
        )

        return questions

    async def get_feedback_question(
        self,
        user_id: UUID,
        question_id: int
    ) -> models.QuestionFeedback | None:
        """"""

        feedback = await self.interview_question_repository.get_feedback_question(user_id, question_id)
        return feedback
