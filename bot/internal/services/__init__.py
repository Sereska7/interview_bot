"""Service layer."""

from dependency_injector import containers, providers

from bot.internal.services import v1


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    v1 = providers.Container(v1.Services)
