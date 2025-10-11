"""Create connection to postgresql."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Union

from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from bot.pkg.connectors import Connectors


__all__ = ["get_connection"]


@asynccontextmanager
async def get_connection(
    session_factory: async_sessionmaker[AsyncSession] = None,
    return_engine: bool = False,
    engine: AsyncEngine = None,
) -> AsyncGenerator[Union[AsyncSession, AsyncEngine], None]:

    # Получаем реальные объекты из контейнера, если не переданы напрямую
    if session_factory is None:
        session_factory = Connectors.postgresql.session_factory()
    if engine is None:
        engine = Connectors.postgresql.engine()

    if return_engine:
        yield engine
        return

    async with session_factory() as session:
        yield session