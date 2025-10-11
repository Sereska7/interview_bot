"""Async resource for PostgresSQL connector."""

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from bot.pkg.connectors.resources import BaseAsyncResource

__all__ = ["Postgresql"]


class Postgresql(BaseAsyncResource):
    """PostgreSQL connector using SQLAlchemy async engine."""

    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.async_session: async_sessionmaker | None = None

    async def init(self, dsn: str, *args: tuple, **kwargs: dict) -> AsyncEngine:
        """Initialize asynchronous SQLAlchemy engine.

        Args:
            dsn: Database connection string. Example:
                 'postgresql+asyncpg://user:pass@host/dbname'

        Returns:
            AsyncEngine instance.
        """

        self.engine = create_async_engine(dsn, *args, **kwargs)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        return self.engine

    async def shutdown(self, resource: AsyncEngine):
        """Dispose SQLAlchemy engine on shutdown."""

        await resource.dispose()
