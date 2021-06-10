import enum


class EnumStr(enum.Enum):
    """An enum in which value and name is the same"""

    def _generate_next_value_(name, start, count, last_values):
        return name
