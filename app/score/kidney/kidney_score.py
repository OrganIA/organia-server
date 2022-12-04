import math

from app import db
from app.db.models import Kidney
from app.errors import NotFoundError
from app.geopy import get_distance
from app.score.kidney.antigen_score import (
    get_age_bonus,
    get_age_malus,
    get_antibody_score,
    get_fag_score,
    getDQScore,
    getDRScore,
)
from app.score.kidney.dialysis_score import get_score, get_waiting_score


def get_H_age(receiver, receiver_listing, listing_kidney):
    return (
        100 * get_score(receiver_listing, listing_kidney)
        + 200 * get_waiting_score(receiver_listing, listing_kidney)
        + (
            100 * get_antibody_score(receiver_listing)
            + 400 * getDRScore(receiver_listing)
            + 100 * getDQScore(receiver_listing)
            + 150 * get_fag_score()
        )
        * get_age_malus(receiver)
        + 750 * get_age_bonus(receiver)
    )


def check_age(receiver, donor):
    if receiver.age - donor.age > 5:
        return 100
    else:
        return abs(receiver.age - donor.age)


def get_differential_age(receiver, donor):
    age = check_age(receiver, donor)
    return 1 / (math.exp(pow(0.02 * age, 0.85)))


def get_score_HD(receiver, donor, receiver_listing, listing_kidney):
    HAge = get_H_age(receiver, receiver_listing, listing_kidney)
    FAge = get_differential_age(receiver, donor)
    if receiver.age > donor.age + 20:
        check = 0
    else:
        check = 1
    return (HAge * check) / FAge


def get_score_MG(hospital_1, hospital_2):
    MG = get_distance(hospital_1, hospital_2)
    return MG


def get_score_NAP(receiver, donor, receiver_listing):
    listing_kidney = (
        db.session.query(Kidney)
        .filter_by(listing_id=receiver_listing.id)
        .first()
    )
    if not listing_kidney:
        raise NotFoundError("No listing found in kidneys table")

    score_HD = get_score_HD(receiver, donor, receiver_listing, listing_kidney)
    score_MG = get_score_MG("MARSEILLE", "PARIS")
    return score_HD * score_MG