from . import client, PREFIX
from .fixtures import clean_db
from .helpers import assert_response
import enum
from app.api.compatibility import (
    compatibility_score,
)


class Rhesus(enum.Enum):
    POSITIVE = '+'
    NEGATIVE = '-'
