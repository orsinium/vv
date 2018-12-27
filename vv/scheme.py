from typing import get_type_hints

from .flags import NOTHING
from .field import Field


def scheme(model: type) -> type:
    hints = get_type_hints(model)

    model._fields = dict()
    for field_name in dir(model):
        if field_name[:2] == '__':
            continue
        model._fields[field_name] = Field(
            name=field_name,
            hint=hints.get(field_name, NOTHING),
            value=getattr(model, field_name),
        )
    for field_name, hint in hints.items():
        if field_name in model._fields:
            continue
        model._fields[field_name] = Field(
            name=field_name,
            hint=hint,
            value=tuple(),
        )

    return model
