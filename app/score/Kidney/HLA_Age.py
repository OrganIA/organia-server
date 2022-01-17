# from app.models import Person, Listing


def getABScore(receiver_listing):
    x = receiver_listing["A"] + receiver_listing["B"]
    if x >= 4:
        return 0
    return (4 - x) / 4


def getDRScore(receiver_listing):
    if receiver_listing["DR"] >= 2:
        return 0
    return (2 - receiver_listing["DR"]) / 2


def getDQScore(receiver_listing):
    if receiver_listing["DQ"] >= 2:
        return 0
    return (2 - receiver_listing["DQ"]) / 2


def getAgeMalus(receiver):
    if receiver["age"] <= 45:
        return 1
    elif receiver["age"] > 75:
        return 0
    return (75 - receiver["age"]) / 30


def getAgeBonus(receiver):
    if receiver["age"] < 45:
        return 0
    elif receiver["age"] >= 100:
        return 1
    return (100 - receiver["age"]) / 55


def getFagScore():
    return 0
