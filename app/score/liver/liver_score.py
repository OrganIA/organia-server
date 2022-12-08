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


def get_score_mg(hospital_1, hospital_2):
    MG = get_distance(hospital_1, hospital_2)
    return MG


def compute_liver_score(donor_organ, receiver_listing):
    donor = donor_organ.listing.person
    receiver = receiver_listing.person
    # donor_listing = donor_organ.listing
    receiver_organ = receiver_listing.organ

    if not receiver_organ:
        raise ValueError("No organ found for receiver")

    if donor.age > 40 and (receiver.age >= 15 and receiver.age < 40):
        return (
            alpha_fetoprotein_score(receiver_organ)
            * meld_score()
            # * get_score_HD(receiver, donor, receiver_listing, donor_listing)
        )
    else:
        return (
            alpha_fetoprotein_score(receiver_organ)
            * meld_score()
            # * get_score_HD(receiver, donor, receiver_listing, donor_listing)
        ) / get_score_mg("PARIS", "MARSEILLE")
