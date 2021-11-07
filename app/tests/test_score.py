from . import client, PREFIX
from .fixtures import clean_db
from .helpers import assert_response
from app.helpers.enums import EnumStr
from app.api.score import (
    organs_priority,
    compute_scoring
)
from app.api.compatibility import (
    compatibility_B,
)
import enum

class Rhesus(enum.Enum):
    POSITIVE = '+'
    NEGATIVE = '-'

class ABO(EnumStr):
    A = enum.auto()
    B = enum.auto()
    AB = enum.auto()
    O = enum.auto()

SAMPLE_LISTING_1 = {
    "start_date": "2021-10-11",
    "end_date": "2021-10-11",
    "notes": "salapsoj",
    "organ": "HEART",
    "donor": 'false',
    "person": {
        "id": 1,
        "created_at": "2021-10-07T17:03:20.177979",
        "updated_at": 'null',
        "first_name": "string",
        "last_name": "string",
        "birthday": "2021-10-07",
        "description": "string",
        "abo": "A",
        "rhesus": "+",
        "gender": "MALE",
        "blood_type": "A+",
        "age": 27
    }
}

SAMPLE_LISTING_2 = {
    "start_date": "2021-10-11",
    "end_date": "2021-10-11",
    "notes": "string",
    "hospital_id": 'null',
    "organ": "HEART",
    "id": 6,
    "person_id": 8,
    "donor": 'true',
    "person": {
        "id": 8,
        "first_name": "David",
        "birthday": "1999-01-18",
        "description": "Californie",
        "blood_type": "B+",
        "gender": "MALE",
        "rhesus": "+",
        "updated_at": 'null',
        "created_at": "2021-10-11T13:30:50.674966",
        "last_name": "Farjon",
        "user_id": 'null',
        "abo": "B",
        "age": 50
    }
}


def compute_scoring(receiver_blood_type, receiver_organ, receiver_age):
    blood_type = compatibility_B(receiver_blood_type, Rhesus.POSITIVE)
    organs_score = organs_priority(receiver_organ)

    age = int(receiver_age)
    # TODO : Add conditions to check the organ and redirect to correct scoring functions
    score = organs_score * (100 + (blood_type + age)) / 3.5
    return score

def test_organs_priority_heart():
    assert organs_priority("HEART") == 1

def test_organs_priority_kidney():
    assert organs_priority("KIDNEYS") == 2

def test_organs_priority_other():
    assert organs_priority(" ") == 3

def test_compute_scoring():
    assert compute_scoring(SAMPLE_LISTING_1["person"]["blood_type"], SAMPLE_LISTING_1["organ"], SAMPLE_LISTING_2["person"]["age"]) == 43.142857142857146