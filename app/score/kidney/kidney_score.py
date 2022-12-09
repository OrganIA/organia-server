import math
from datetime import datetime

from app.errors import NotFoundError
from app.geopy import get_distance
from app.score.kidney.antigen_score import (
    get_age_bonus,
    get_age_malus,
    get_antibody_score,
    getDQScore,
    getDRScore,
)
from app.score.kidney.dialysis_score import get_score, get_waiting_score


def get_H_age(receiver, receiver_listing, listing_kidney):
    current_date = datetime.utcnow().date()
    return (
        100 * get_score(receiver_listing, listing_kidney, current_date)
        + 200
        * get_waiting_score(receiver_listing, listing_kidney, current_date)
        + (
            100 * get_antibody_score(receiver_listing)
            + 400 * getDRScore(receiver_listing)
            + 100 * getDQScore(receiver_listing)
            # + 150 * facilité d'accès à la greffe 0 | 1
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
    return get_distance(hospital_1, hospital_2) or 1


def compute_kidney_score(donor_listing, receiver_listing):
    listing_kidney = receiver_listing.organ
    receiver = receiver_listing.person
    donor = donor_listing.person

    if not listing_kidney:
        raise NotFoundError("No listing found in kidneys table")

    score_HD = get_score_HD(receiver, donor, receiver_listing, listing_kidney)
    mg = 1
    if receiver_listing.hospital and donor_listing.hospital:
        try:
            mg = get_score_MG(
                receiver_listing.hospital.name, donor_listing.hospital.name
            )
        except Exception:
            pass
    return score_HD * mg
