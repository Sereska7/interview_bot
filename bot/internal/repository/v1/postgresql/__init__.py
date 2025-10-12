"""All postgresql repositories are defined here."""

from dependency_injector import containers, providers

from bot.internal.repository.v1.postgresql.question import QuestionRepository
from bot.internal.repository.v1.postgresql.user import UserRepository


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    user_repository = providers.Factory(UserRepository)
    question_repository = providers.Factory(QuestionRepository)
