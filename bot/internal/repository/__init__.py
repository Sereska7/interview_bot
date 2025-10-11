from dependency_injector import containers, providers

from bot.internal.repository import v1

__all__ = ["Repositories"]


class Repositories(containers.DeclarativeContainer):
    """Container for repositories.

    Attributes:
        ыpostgresql (providers.Container): Container for postgresql repositories.

    Notes:
        If you want to add a new repository,
        you **must** add it to this container.
    """

    v1 = providers.Container(v1.Repositories)
