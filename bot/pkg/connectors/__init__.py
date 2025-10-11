"""All connectors in declarative container."""

from dependency_injector import containers, providers

from bot.pkg.settings import settings
from bot.pkg.connectors.postgresql import PostgresSQL


__all__ = ["Connectors", "PostgresSQL"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with all connectors."""

    configuration = providers.Configuration(name="settings")
    configuration.from_dict(settings.model_dump())

    postgresql: PostgresSQL = providers.Container(PostgresSQL)
