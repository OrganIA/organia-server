from . import client, PREFIX
from .fixtures import clean_db
from .helpers import assert_response
from app.helpers.enums import EnumStr
from app.models import Person
from app.models import Listing
from app.api.score import (
    organs_priority,
    compute
)


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


def test_organs_priority_heart():
    assert organs_priority("HEART") == 1


def test_organs_priority_kidney():
    assert organs_priority("KIDNEYS") == 2


def test_organs_priority_other():
    assert organs_priority(" ") == 3


# def test_compute_scoring():
#     assert compute_scoring(SAMPLE_LISTING_1["person"]["blood_type"],
#         SAMPLE_LISTING_1["organ"],
#         SAMPLE_LISTING_2["person"]["age"]) == 43.142857142857146
