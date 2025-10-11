"""Optional field function for pydantic models."""

from typing import Any

from pydantic.fields import FieldInfo

__all__ = ["OptionalField", "create_optional_fields_class"]


def OptionalField(field: FieldInfo, default: Any = None) -> FieldInfo:  # noqa
    """Takes an already created Field and makes it optional by adding a default
    value to it.

    Args:
        field (FieldInfo): Field to make optional.
        default (Any, optional): Default value. Defaults to None.

    Returns:
        FieldInfo: Optional field.
    """

    return field.merge_field_infos(field, default=default)


def create_optional_fields_class(base_cls):
    """Function to create a new class with all fields made optional.

    Args:
        base_cls: Class to make all fields optional.

    Returns:
        Class: New class with all fields optional.
    """
    new_attrs = {}
    for attr_name, attr_value in base_cls.__dict__.items():
        if attr_name.startswith("__") and attr_name.endswith("__"):
            continue
        if isinstance(attr_value, FieldInfo):
            new_attrs[attr_name] = OptionalField(attr_value)
        else:
            new_attrs[attr_name] = attr_value
    return type(f"Optional{base_cls.__name__}", base_cls.__bases__, new_attrs)
