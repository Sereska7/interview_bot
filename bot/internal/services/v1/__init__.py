"""V1 services layer."""

from dependency_injector import containers, providers

from bot.internal.repository import Repositories
from bot.internal.repository.v1 import postgresql
from bot.internal.services.v1.question import QuestionService
from bot.internal.services.v1.result import ResultService
from bot.internal.services.v1.session import SessionService
from bot.internal.services.v1.user import UserService
from bot.pkg.settings import settings


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    configuration = providers.Configuration(name="settings")
    configuration.from_dict(settings.model_dump())


    postgres_repositories: postgresql.Repositories = providers.Container(
        Repositories.v1.postgres,
    )  # type: ignore

    user_service = providers.Factory(UserService)
    user_service.add_attributes(
        user_repository=postgres_repositories.user_repository,
    )

    question_service = providers.Factory(QuestionService)
    question_service.add_attributes(
        question_repository=postgres_repositories.question_repository,
    )

    result_service = providers.Factory(ResultService)
    result_service.add_attributes(
        result_repository=postgres_repositories.result_repository
    )

    session_service = providers.Factory(SessionService)
    session_service.add_attributes(
        session_repository=postgres_repositories.session_repository,
    )
