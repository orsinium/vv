import re
from typing import Optional, Any
from inspect import formatannotation
from enum import Enum

from .flags import NOTHING


rex_optional = re.compile(r'Union\[.*\, NoneType\]')


class Field:
    slug: str               # example: first_name
    name: str               # example: First Name
    hint: Optional[str]     # example: Union[str, int]
    optional: bool
    choices: Optional[Enum] = None
    description: Optional[str] = None

    def __init__(self, name: str, value: Any, hint: Any = NOTHING):
        self.name = self.slug = name

        if isinstance(hint, NOTHING):
            hint = None
        elif not isinstance(hint, str):
            # In Python 4.0 all annotations will be strings. So, we have to be ready.
            hint: str = formatannotation(hint)
        self.hint = hint

        self.optional = self.hint.startswith('Optional[') or rex_optional.fullmatch(self.hint)

        if not isinstance(value, (list, tuple)):
            value = (value, )
        if not value:
            return
        if isinstance(value[0], str):
            self.name = value[0]
            value = value[1:]

        for rule in value:
            self._attach(rule)

    def _attach(self, rule):
        if isinstance(rule, str):
            self.description = rule
            return
        if isinstance(rule, Enum):
            self.choices = rule
            return

    def __repr__(self) -> str:
        return '{}({})'.format(type(self), self.name)
