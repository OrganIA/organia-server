import math

from app import db
from app.db.models import Kidney
from app.distance import get_distance
from app.errors import NotFoundError
from app.score.Kidney.DialyseScore import getScore, getWaitingScore
from app.score.Kidney.HLA_Age import (
    getABScore,
    getAgeBonus,
    getAgeMalus,
    getDQScore,
    getDRScore,
    getFagScore,
)


def getHAge(receiver, receiver_listing, listing_kidney):
    return (
        100 * getScore(receiver_listing, listing_kidney)
        + 200 * getWaitingScore(receiver_listing, listing_kidney)
        + (
            100 * getABScore(receiver_listing)
            + 400 * getDRScore(receiver_listing)
            + 100 * getDQScore(receiver_listing)
            + 150 * getFagScore()
        )
        * getAgeMalus(receiver)
        + 750 * getAgeBonus(receiver)
    )
    # + 200 * getWaitingScore(receiver_listing, listing_kidney) \


def checkAge(receiver, donor):
    if receiver.age - donor.age > 5:
        return 100
    else:
        return abs(receiver.age - donor.age)


def getDifferentialAge(receiver, donor):
    age = checkAge(receiver, donor)
    return 1 / (math.exp(pow(0.02 * age, 0.85)))


def getScoreHD(receiver, donor, receiver_listing, listing_kidney):
    HAge = getHAge(receiver, receiver_listing, listing_kidney)
    FAge = getDifferentialAge(receiver, donor)
    if receiver.age > donor.age + 20:
        check = 0
    else:
        check = 1
    return (HAge * check) / FAge


def getScoreMG(hospital_1, hospital_2):
    MG = get_distance(hospital_1, hospital_2)
    return MG


def getScoreNAP(receiver, donor, receiver_listing):
    # print(receiver_listing.id)
    listing_kidney = (
        db.session.query(Kidney)
        .filter_by(listing_id=receiver_listing.id)
        .first()
    )
    # print(listing_kidney)
    if not listing_kidney:
        raise NotFoundError("No listing found in kidneys table")

    ScoreHD = getScoreHD(receiver, donor, receiver_listing, listing_kidney)
    MGScore = getScoreMG("MARSEILLE", "PARIS")
    return ScoreHD * MGScore
