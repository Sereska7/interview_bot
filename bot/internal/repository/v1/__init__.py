"""Repository container."""

from dependency_injector import containers, providers

from bot.internal.repository.v1 import postgresql

__all__ = ["Repositories"]


class Repositories(containers.DeclarativeContainer):
    """Container for repositories.

    Attributes:
        postgres (providers.Container): Container for postgresql repositories.

    Notes:
        If you want to add a new repository,
        you **must** add it to this container.
    """

    postgres = providers.Container(postgresql.Repositories)
