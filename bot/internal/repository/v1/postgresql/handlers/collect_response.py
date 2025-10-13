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


def collect_response(fn: Callable) -> Callable:
    @wraps(fn)
    async def inner(*args: Any, **kwargs: Any) -> Any:
        response = await fn(*args, **kwargs)
        return await process_response(fn, response)
    return inner

async def process_response(fn: Callable, response: Any) -> Any:
    return_annotation = get_type_hints(fn).get("return")
    if return_annotation is None or return_annotation is type(None):
        return None

    origin = get_origin(return_annotation)
    args = get_args(return_annotation)

    # Проверяем Optional
    is_optional = origin is Union and type(None) in args
    base_type = None
    if is_optional:
        base_type = [t for t in args if t is not type(None)][0]
        if response is None:
            return None
    else:
        base_type = return_annotation

    base_origin = get_origin(base_type)

    # Если возвращается список
    if base_origin is list or base_origin is List:
        item_type = get_args(base_type)[0]
        adapter = TypeAdapter(item_type)

        # Если response не список, принудительно оборачиваем
        if not isinstance(response, list):
            response = [response]

        return [adapter.validate_python(obj, from_attributes=True) for obj in response]

    # Если возвращается одиночная модель
    adapter = TypeAdapter(base_type)
    return adapter.validate_python(response, from_attributes=True)
