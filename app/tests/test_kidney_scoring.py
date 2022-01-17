import datetime
from app.score.Kidney.HLA_Age import getABScore, getAgeBonus, getAgeMalus, getDQScore, getDRScore, getFagScore
from app.score.Kidney.DialyseScores import getDate, getScore, getWaitingScore

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
        "startDateDialyse": datetime.datetime(2021, 11, 1),
        "EndDateDialyse": datetime.datetime(2021, 12, 1),
        "DateTransplantation": datetime.datetime(2021, 12, 2),
        "ReRegistrationDate": None,
        "ARFDate": None,

        "start_date": datetime.datetime(2021, 11, 1),

        "A": 0,
        "B": 0,
        "DR": 0,
        "DQ": 0
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

def test_getDate():
    assert getDate(SAMPLE_LISTING_3["receiver_listing"]) == SAMPLE_LISTING_3["receiver_listing"]["startDateDialyse"]

def test_DD():
    assert getScore(SAMPLE_LISTING_3["receiver_listing"]) == 0.021369863013698632


def test_DA():
    assert getWaitingScore(SAMPLE_LISTING_3["receiver_listing"]) == 0.65


def test_ABScore():
    assert getABScore(SAMPLE_LISTING_3["receiver_listing"]) == 1


def test_DQScore():
    assert getDQScore(SAMPLE_LISTING_3["receiver_listing"]) == 1


def test_DRScore():
    assert getDRScore(SAMPLE_LISTING_3["receiver_listing"]) == 1


def test_getFagScore():
    assert getFagScore() == 0


def test_getAgeMalus():
    assert getAgeMalus(SAMPLE_LISTING_3["person"]) == 0.8333333333333334


def test_getAgeBonus():
    assert getAgeBonus(SAMPLE_LISTING_3["person"]) == 0.9090909090909091
