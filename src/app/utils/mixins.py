"""
Mixins for reusable Python behaviors.
"""
import enum


class StringEnumMixin(str, enum.Enum):
    """
    Helper class for string enums where ``str(member)`` prints the value.
    """
    def __str__(self) -> str:
        return str.__str__(self)
