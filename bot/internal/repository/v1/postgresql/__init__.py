"""All postgresql repositories are defined here."""

from dependency_injector import containers, providers

from bot.internal.repository.v1.postgresql.category import CategoryRepository
from bot.internal.repository.v1.postgresql.interview_repository import InterviewQuestionRepository
from bot.internal.repository.v1.postgresql.question import QuestionRepository
from bot.internal.repository.v1.postgresql.question_feedback_repository import QuestionFeedbackRepository
from bot.internal.repository.v1.postgresql.result import ResultRepository
from bot.internal.repository.v1.postgresql.user import UserRepository
from bot.internal.repository.v1.postgresql.user_profile import UserProfileRepository
from bot.internal.repository.v1.session import SessionRepository


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    user_repository = providers.Factory(UserRepository)
    user_profile_repository = providers.Factory(UserProfileRepository)
    question_repository = providers.Factory(QuestionRepository)
    result_repository = providers.Factory(ResultRepository)
    session_repository = providers.Factory(SessionRepository)
    interview_question_repository = providers.Factory(InterviewQuestionRepository)
    question_feedback_repository = providers.Factory(QuestionFeedbackRepository)
    category_repository = providers.Factory(CategoryRepository)
