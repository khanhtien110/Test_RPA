from enum import Enum


def is_null_or_empty(value):
    return value is None or not value.strip()


def is_1d_array(data):
    return isinstance(data, list) and all(not isinstance(i, list) for i in data)

def is_2d_array(data):
    return isinstance(data, list) and all(isinstance(i, list) for i in data)

class Direction(Enum):
    AUTO = (1,)
    VERTICAL = (2,)
    HORIZONTAL = (3,)
