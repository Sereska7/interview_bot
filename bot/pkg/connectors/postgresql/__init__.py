"""Container with PostgreSQL connector using SQLAlchemy async."""

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.pkg.connectors.postgresql.resource import Postgresql
from bot.pkg.settings import settings

__all__ = ["PostgresSQL"]


class PostgresSQL(containers.DeclarativeContainer):
    """Declarative container with async SQLAlchemy PostgreSQL connector."""

    configuration = providers.Configuration(name="settings")
    configuration.from_dict(settings.model_dump())

    engine = providers.Singleton(
        create_async_engine,
        url=configuration.POSTGRES.DSN,
        echo=configuration.POSTGRES.ECHO,
        pool_size=configuration.POSTGRES.MIN_CONNECTION,
        future=True,
    )

    session_factory = providers.Singleton(
        async_sessionmaker,
        bind=engine,
        expire_on_commit=False,
    )


class TestPostgresSQL(containers.DeclarativeContainer):
    """Declarative container with test async SQLAlchemy PostgreSQL
    connector."""

    configuration = providers.Configuration(name="settings")
    configuration.from_dict(settings.model_dump())

    engine = providers.Singleton(
        create_async_engine,
        url=configuration.POSTGRES.TEST_DSN,
        echo=configuration.POSTGRES.ECHO,
        pool_size=configuration.POSTGRES.MIN_CONNECTION,
        future=True,
    )

    session_factory = providers.Singleton(
        async_sessionmaker,
        bind=engine,
        expire_on_commit=False,
    )
