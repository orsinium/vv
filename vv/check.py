from typing import Any, List, Dict
from enum import Enum

from typeguard import check_type

from .field import Field
from .flags import NOTHING


def _check_choices(choices: Enum, value: Any) -> bool:
    if value[:2] == '__':
        return False
    # check choice name
    if value in dir(choices):
        return True
    # check choice instance
    if isinstance(value, choices):
        return True
    # check choice value
    if value in (item.value for item in choices):
        return True
    return False


def _check_field(field: Field, value: Any) -> List[str]:
    # check typing
    if field.hint is not NOTHING:
        try:
            check_type(
                argname=field.name,
                value=value,
                expected_type=field.hint,
            )
        except TypeError as e:
            return list(e.args)

    errors = []
    # check choices
    if field.choices is not None:
        if not _check_choices(field.choices, value):
            errors.append('value not in list of available values')
    return errors


def check(model: type, data: Dict[str, Any]) -> Dict[str, List[str]]:
    errors = dict()
    for field in model._fields:
        if field.slug not in data:
            if field.optional:
                continue
            else:
                errors[field.slug] = ['field is required']
        else:
            field_errors = _check_field(field=field, value=data[field.slug])
            if field_errors:
                errors[field.slug] = field_errors
    return errors
