import math

from app.geopy import get_distance

# from app.score.kidney.kidney_score import get_score_HD


def alpha_fetoprotein_score(receiver_listing):
    if (
        receiver_listing.organ.tumors_number == 0
        or receiver_listing.organ.biggest_tumor_size is None
        or receiver_listing.organ.alpha_fetoprotein is None
    ):
        return 0
    alpha_fetoprotein_score = 0
    if receiver_listing.organ.tumors_number >= 4:
        alpha_fetoprotein_score += 2
    if (
        receiver_listing.organ.biggest_tumor_size > 3
        and receiver_listing.organ.biggest_tumor_size <= 6
    ):
        alpha_fetoprotein_score += 1
    elif receiver_listing.organ.biggest_tumor_size > 6:
        alpha_fetoprotein_score += 4
    if (
        receiver_listing.organ.alpha_fetoprotein > 100
        and receiver_listing.organ.alpha_fetoprotein <= 1000
    ):
        alpha_fetoprotein_score += 2
    elif receiver_listing.organ.alpha_fetoprotein > 1000:
        alpha_fetoprotein_score += 3
    return alpha_fetoprotein_score


def meld_score():
    meld = (
        10 * (0.957 * math.log(4))
        + (0.378 * math.log(0.0113))
        + (1.120 * math.log(1))
        + 0.6431
    )
    return meld


def get_score_mg(hospital_1, hospital_2):
    MG = get_distance(hospital_1, hospital_2)
    return MG


def final_score(receiver, donor):
    if donor.person.age > 40 and (
        receiver.person.age >= 15 and receiver.person.age < 40
    ):
        return (
            alpha_fetoprotein_score(receiver)
            * meld_score()
            # * get_score_HD(receiver, donor, receiver_listing.organ, donor_listing)
        )
    else:
        return (
            alpha_fetoprotein_score(receiver)
            * meld_score()
            # * get_score_HD(receiver, donor, receiver_listing.organ, donor_listing)
        ) / get_score_mg("Hopital Robert Ballanger", "Paul D'Eugine")
