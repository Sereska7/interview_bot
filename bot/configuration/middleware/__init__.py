from dependency_injector import containers, providers
from bot.configuration.middleware.user_context_middleware import UserContextMiddleware
from bot.internal.services.v1 import Services as V1Services


class Middlewares(containers.DeclarativeContainer):
    v1_services = providers.Container(V1Services)

    user_context_middleware = providers.Factory(
        UserContextMiddleware
    )
    user_context_middleware.add_attributes(
        user_service=v1_services.user_service,
        user_profile_service=v1_services.user_profile_service,
    )