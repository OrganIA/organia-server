import enum


class EnumStr(enum.Enum):
    """An enum in which value and name is the same"""

    def _generate_next_value_(
        name, start, count, last_values  # noqa: N805 first argument is self
    ):
        return name

    @classmethod
    def values(cls):
        return [x.value for x in cls]
