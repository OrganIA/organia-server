import math

from app.geopy import get_distance


def alpha_fetoprotein_score(receiver_organ):
    if (
        receiver_organ.tumors_count == 0
        or receiver_organ.biggest_tumor_size is None
        or receiver_organ.alpha_fetoprotein is None
    ):
        return 0
    alpha_fetoprotein_score = 0
    if receiver_organ.tumors_count >= 4:
        alpha_fetoprotein_score += 2
    if (
        receiver_organ.biggest_tumor_size > 3
        and receiver_organ.biggest_tumor_size <= 6
    ):
        alpha_fetoprotein_score += 1
    elif receiver_organ.biggest_tumor_size > 6:
        alpha_fetoprotein_score += 4
    if (
        receiver_organ.alpha_fetoprotein > 100
        and receiver_organ.alpha_fetoprotein <= 1000
    ):
        alpha_fetoprotein_score += 2
    elif receiver_organ.alpha_fetoprotein > 1000:
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


def get_score_MG(hospital_1, hospital_2):
    return get_distance(hospital_1, hospital_2) or 1


def compute_liver_score(donor_listing, receiver_listing):
    donor = donor_listing.person
    receiver = receiver_listing.person
    receiver_organ = receiver_listing.organ

    if not receiver_organ:
        raise ValueError("No organ found for receiver")

    score = alpha_fetoprotein_score(receiver_organ) * meld_score()
    if donor.age > 40 and (receiver.age >= 15 and receiver.age < 40):
        return score
    mg = 1
    if receiver_listing.hospital and donor_listing.hospital:
        try:
            mg = get_score_MG(
                receiver_listing.hospital.name, donor_listing.hospital.name
            )
        except Exception:
            pass
    return score * mg
