from app.score.Kidney.HLA_Age import *
from app.score.Kidney.DialyseScores import *

SAMPLE_LISTING_3 = {
    "start_date": "2021-10-11",
    "end_date": "2021-12-11",
    "notes": "string",
    "hospital_id": 'null',
    "organ": "KIDNEY",
    "id": 6,
    "person_id": 8,
    "donor": False,

    "receiver_listing": {
        "isDialyse": True,
        "isRetransplantation": False,
        "startDateDialyse": "2021-11-01",
        "EndDateDialyse": "2021-12-01",
        "DateTransplantation": "2021-12-02",
        "ReRegistrationDate": None,
        "ARFDate": None,

        "start_date": "2021-11-01",

    },

    "person": {
        "id": 8,
        "first_name": "David",
        "birthday": "1999-01-18",
        "description": "Californie",
        "blood_type": "B+",
        "gender": "MALE",
        "rhesus": "+",
        "updated_at": None,
        "created_at": "2021-10-11T13:30:50.674966",
        "last_name": "Farjon",
        "user_id": None,
        "abo": "B",
        "age": 50
    }
}


def test_DD():
    assert getScore(SAMPLE_LISTING_3["receiver_listing"]) == SAMPLE_LISTING_3["receiver_listing"].startDateDialyse

def test_DA():
    assert getWaitingScore(SAMPLE_LISTING_3["receiver_listing"]) == 1

def test_ABScore():
    assert getABScore() == 1

def test_DRScore():
    assert getDQScore() == 1

def test_getFagScore():
    assert getFagScore() == 1

def test_getAgeMalus():
    assert getAgeMalus(SAMPLE_LISTING_3["person"]) == 0.83333333333

def test_getAgeBonus():
    assert getAgeBonus(SAMPLE_LISTING_3["receiver_listing"]) == 0.90909090909
