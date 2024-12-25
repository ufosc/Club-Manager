"""
Type utilities.
"""

from typing import Optional, TypeVar


T = TypeVar("T")


def islisttype(target: Optional[list], class_or_tuple, /):
    if target is None:
        return False
    elif len(target) == 0:
        return True

    return isinstance(target[0], class_or_tuple)
