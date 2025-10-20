"""All postgresql repositories are defined here."""

from dependency_injector import containers, providers

from bot.internal.repository.v1.postgresql.question import QuestionRepository
from bot.internal.repository.v1.postgresql.result import ResultRepository
from bot.internal.repository.v1.postgresql.user import UserRepository
from bot.internal.repository.v1.session import SessionRepository


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    user_repository = providers.Factory(UserRepository)
    question_repository = providers.Factory(QuestionRepository)
    result_repository = providers.Factory(ResultRepository)
    session_repository = providers.Factory(SessionRepository)
