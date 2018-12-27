import re
from typing import Optional, Any, List
from enum import Enum
from typing import Callable

from .flags import NOTHING, default


rex_optional = re.compile(r'Union\[.*\, NoneType\]')
rex_type = type(rex_optional)


class Field:
    slug: str               # example: 'first_name'
    name: str               # example: 'First Name'
    hint: Any               # example: Union[str, int]

    optional: bool = False
    choices: Optional[Enum] = None
    description: Optional[str] = None
    default: Optional[Any] = None
    validators: List[callable] = None

    def __init__(self, name: str, value: Any, hint: Any = NOTHING):
        self.name = self.slug = name
        self.validators = []

        if not isinstance(value, (list, tuple)):
            value = (value, )
        if not value:
            return
        if isinstance(value[0], str):
            self.name = value[0]
            value = value[1:]

        for rule in value:
            self._attach(rule)

    def _attach(self, rule: Any) -> None:
        if isinstance(rule, str):
            self.description = rule
            return
        if isinstance(rule, Enum):
            self.choices = rule
            return
        if isinstance(rule, default):
            self.default = rule.value
            return
        if isinstance(rule, Callable):
            self.validators.append(rule)
            return
        if isinstance(rule, rex_type):
            self.validators.append(rule.fullmatch)
            return

    def __repr__(self) -> str:
        return '{}({})'.format(type(self), self.name)
