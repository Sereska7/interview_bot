from bot.internal.repository.v1.postgresql import question_feedback_repository
from bot.internal.repository.v1.postgresql.question_feedback_repository import QuestionFeedbackRepository
from bot.pkg.models import v1 as models

class QuestionFeedbackService:
    """"""

    question_feedback_repository: QuestionFeedbackRepository

    async def create_feedback(
        self,
        cmd: models.QuestionFeedbackCreateCommand
    ) -> models.QuestionFeedback:
        """"""

        return await self.question_feedback_repository.create_feedback(cmd)

    async def get_feedback_by_user_and_question(self, user_id: int, question_id: int):
        return await self.question_feedback_repository.read_by_user_and_question(user_id, question_id)

