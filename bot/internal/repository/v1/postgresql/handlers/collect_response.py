"""Collect response module."""

from functools import wraps
from typing import (
    Any,
    Callable,
    List,
    Type,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from pydantic import TypeAdapter

from bot.internal.repository.v1.postgresql.handlers.handle_exception import (
    handle_exception,
)
from bot.pkg.models.base import Model


def collect_response(fn) -> Callable:
    @wraps(fn)
    @handle_exception
    async def inner(
        *args: Any,
        **kwargs: Any,
    ) -> Union[List[Type[Model]], Type[Model], None]:
        response = await fn(*args, **kwargs)
        return await process_response(fn, response)

    return inner


async def process_response(
    fn: Callable,
    response: Any,
) -> Union[List[Type[Model]], Type[Model], None]:
    return_annotation = get_type_hints(fn).get("return")
    if return_annotation is None or return_annotation is type(None):
        return None

    origin = get_origin(return_annotation)
    is_optional = origin is Union and type(None) in get_args(return_annotation)

    if is_optional and not response:
        return None

    if origin is list and not response:
        return []

    if not response:
        raise Exception

    base_type = None
    if is_optional:
        base_type = [t for t in get_args(return_annotation) if t is not type(None)][0]
    else:
        base_type = return_annotation

    adapter = TypeAdapter(base_type)

    if origin is list:
        return [adapter.validate_python(obj) for obj in response]

    return adapter.validate_python(response)
