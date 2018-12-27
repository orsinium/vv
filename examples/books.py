import re
from datetime import date
from enum import Enum
from typing import List

from vv import default, value, Error, errors, scheme, optional


errors.register('title', '{name} ({value}) should start with capital letter')
# ^ Example: "First Name (first_name) should start with capital letter."


class Sex(Enum):
    FEMALE = 0
    MALE = 1


@scheme
class Author:
    first_name: str = ('First Name', value.istitle(), Error('title'))
    # ^ 1. If first parameter is string, it's field verbose name.
    # ^ 2. `value` is lambda replacement with MagicMock behaivor
    # ^     (https://github.com/kachayev/fn.py).
    # ^ 3. We can pass Error(slug) that will be returned if validator returns False.
    #       If we need more than one error, validator can return Error object itself.
    last_name: str = ('Last Name', value.istitle(), Error('title'), optional)
    # ^ optional parameter
    sex: str = (Sex, default(Sex.FEMALE))
    # ^ 1. enum.Enum will be interpreted as choice.
    # ^ 2. Also we can pass default value via `default(...)`.
    # ^ 3. If verbose name missed, it will be automatically generated from field name.
    hometown: str
    # ^ Yeah, you can miss any params, of course.
    birthday: date = (optional, lambda d: 0 < (date.today() - d) < 150 * 365)
    # ^ Sometimes we have complicated validator that can't be covered by `value`


@scheme
class Book:
    title: str
    authors: List[Author] = len(value) >= 1
    # ^ We can create many-to-many relation in type hints format.
    isbn: str = ('ISBN', re.compile(r'[0-9-]+'), 'International Standard Book Number')
    # ^ 1. Regexp object also will be interpreted as validator
    # ^ 2. Str not in first position will be interpreted as help text.
