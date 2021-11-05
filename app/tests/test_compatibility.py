from . import client, PREFIX
from .fixtures import clean_db
from .helpers import assert_response
from app.api.compatibility import (
    compatibility_O,
    compatibility_A,
    compatibility_B,
    compatibility_AB
)

rhesus_neg = '-'
rhesus_positive = '+'


def test_compatibility_O_negative():
    score = compatibility_O('O+', rhesus_neg)
    assert score == 9
    score = compatibility_O('AB+', rhesus_neg)
    assert score == 10
    score = compatibility_O('A-', rhesus_neg)
    assert score == 9
    score = compatibility_O('B+', rhesus_neg)
    assert score == 10


def test_compatibility_O_positive():
    score = compatibility_O('O+', rhesus_positive)
    assert score == 5
    score = compatibility_O('AB+', rhesus_positive)
    assert score == 9
    score = compatibility_O('A+', rhesus_positive)
    assert score == 5
    score = compatibility_O('B+', rhesus_positive)
    assert score == 8


def test_compatibility_A_negative():
    score = compatibility_A('AB+', rhesus_neg)
    assert score == 10
    score = compatibility_A('A-', rhesus_neg)
    assert score == 9


def test_compatibility_A_positive():
    score = compatibility_A('AB+', rhesus_positive)
    assert score == 5
    score = compatibility_A('A+', rhesus_positive)
    assert score == 5


def test_compatibility_B_negative():
    score = compatibility_B('B-', rhesus_neg)
    assert score == 10
    score = compatibility_B('AB+', rhesus_neg)
    assert score == 10


def test_compatibility_B_positive():
    score = compatibility_B('AB+', rhesus_positive)
    assert score == 9
    score = compatibility_B('B+', rhesus_positive)
    assert score == 8


def test_compatibility_AB_negative():
    score = compatibility_AB('AB+', rhesus_neg)
    assert score == 10


def test_compatibility_AB_positive():
    score = compatibility_AB('AB+', rhesus_positive)
    assert score == 9


def test_no_compatibility():
    score = compatibility_AB('B-', rhesus_neg)
    assert score == 1
