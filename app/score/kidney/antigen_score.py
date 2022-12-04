from app.db.models import Listing, Person


def get_antibody_score(receiver_listing: Listing):
    x = receiver_listing.A + receiver_listing.B
    if x >= 4:
        return 0
    return (4 - x) / 4


def getDRScore(receiver_listing: Listing):
    # Donor balance and essential recipient for transplantation
    if receiver_listing.DR >= 2:
        return 0
    return (2 - receiver_listing.DR) / 2


def getDQScore(receiver_listing: Listing):
    # Donor balance and essential recipient for transplantation
    if receiver_listing.DQ >= 2:
        return 0
    return (2 - receiver_listing.DQ) / 2


def get_age_malus(receiver: Person):
    if receiver.age <= 45:
        return 1
    if receiver.age > 75:
        return 0
    return (75 - receiver.age) / 30


def get_age_bonus(receiver: Person):
    if receiver.age < 45:
        return 0
    if receiver.age >= 100:
        return 1
    return (100 - receiver.age) / 55


def get_fag_score():
    # FAG states for "Facilité d'accès à la greffe"
    return 0
