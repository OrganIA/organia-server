from . import client, PREFIX
from .fixtures import clean_db
from .helpers import assert_response
import enum
from app.api.compatibility import (
    compatibility_O,
    compatibility_A,
    compatibility_B,
    compatibility_AB
)


class Rhesus(enum.Enum):
    POSITIVE = '+'
    NEGATIVE = '-'


def test_compatibility_O_negative():
    score = compatibility_O('O+', Rhesus.NEGATIVE)
    assert score == 9
    score = compatibility_O('O-', Rhesus.NEGATIVE)
    assert score == 9
    score = compatibility_O('AB+', Rhesus.NEGATIVE)
    assert score == 10
    score = compatibility_O('AB-', Rhesus.NEGATIVE)
    assert score == 10
    score = compatibility_O('A+', Rhesus.NEGATIVE)
    assert score == 9
    score = compatibility_O('A-', Rhesus.NEGATIVE)
    assert score == 9
    score = compatibility_O('B+', Rhesus.NEGATIVE)
    assert score == 10
    score = compatibility_O('B-', Rhesus.NEGATIVE)
    assert score == 10


def test_compatibility_O_positive():
    score = compatibility_O('O+', Rhesus.POSITIVE)
    assert score == 5
    score = compatibility_O('AB+', Rhesus.POSITIVE)
    assert score == 9
    score = compatibility_O('A+', Rhesus.POSITIVE)
    assert score == 5
    score = compatibility_O('B+', Rhesus.POSITIVE)
    assert score == 8


def test_compatibility_A_negative():
    score = compatibility_A('AB+', Rhesus.NEGATIVE)
    assert score == 10
    score = compatibility_A('AB-', Rhesus.NEGATIVE)
    assert score == 10
    score = compatibility_A('A+', Rhesus.NEGATIVE)
    assert score == 9
    score = compatibility_A('A-', Rhesus.NEGATIVE)
    assert score == 9


def test_compatibility_A_positive():
    score = compatibility_A('AB+', Rhesus.POSITIVE)
    assert score == 5
    score = compatibility_A('A+', Rhesus.POSITIVE)
    assert score == 5


def test_compatibility_B_negative():
    score = compatibility_B('AB+', Rhesus.NEGATIVE)
    assert score == 10
    score = compatibility_B('AB-', Rhesus.NEGATIVE)
    assert score == 10
    score = compatibility_B('B+', Rhesus.NEGATIVE)
    assert score == 10
    score = compatibility_B('B-', Rhesus.NEGATIVE)
    assert score == 10


def test_compatibility_B_positive():
    score = compatibility_B('AB+', Rhesus.POSITIVE)
    assert score == 9
    score = compatibility_B('B+', Rhesus.POSITIVE)
    assert score == 8


def test_compatibility_AB_negative():
    score = compatibility_AB('AB+', Rhesus.NEGATIVE)
    assert score == 10
    score = compatibility_A('AB-', Rhesus.NEGATIVE)
    assert score == 10


def test_compatibility_AB_positive():
    score = compatibility_AB('AB+', Rhesus.POSITIVE)
    assert score == 9

def test_no_compatibility():
    score = compatibility_O('TEST', Rhesus.POSITIVE)
    assert score == 1
    score = compatibility_A('TEST', Rhesus.POSITIVE)
    assert score == 1
    score = compatibility_B('TEST', Rhesus.POSITIVE)
    assert score == 1
    score = compatibility_AB('TEST', Rhesus.POSITIVE)
    assert score == 1
