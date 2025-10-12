"""Handle Postgresql Query Exceptions."""

from typing import Any, Callable, Coroutine

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from bot.pkg.logger import get_logger
from bot.pkg.models.base import Model

logger = get_logger(__name__)


def handle_exception(
    func: Callable[..., Model],
) -> Callable[[tuple[object, ...], dict[str, object]], Coroutine[Any, Any, Model]]:
    """Decorator catching SQLAlchemy async exceptions."""

    async def wrapper(*args: object, **kwargs: object) -> Model:
        try:
            return await func(*args, **kwargs)
        except IntegrityError as error:
            if "unique constraint" in str(error).lower():
                logger.exception(f"Unique constraint violation: {error}")
                raise Exception

            logger.exception(f"Integrity error: {error}")
            raise Exception

        except SQLAlchemyError as error:
            logger.exception(f"SQLAlchemy error: {error}")
            raise Exception

    return wrapper
