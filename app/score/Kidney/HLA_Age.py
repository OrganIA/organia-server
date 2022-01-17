from typing import List
from app import db
from app.models import Person, Listing


HLA_SCORE = {
    "A": 0,
    "B": 0,
    "DR": 0,
    "DQ": 0
}


def HLA_Getter():
    HLA_SCORE["A"] = db.session.query(Listing)\
        .filter((Listing.hla == 'A')).count()
    HLA_SCORE["B"] = db.session.query(Listing)\
        .filter((Listing.hla == 'B')).count()
    HLA_SCORE["DR"] = db.session.query(Listing)\
        .filter((Listing.hla == 'DR')).count()
    HLA_SCORE["DQ"] = db.session.query(Listing)\
        .filter((Listing.hla == 'DQ')).count()
    return HLA_SCORE


def getABScore():
    x = HLA_SCORE["A"] + HLA_SCORE["B"] 
    if x >= 4:
        return 0
    return (4 - x) / 4


def getDRScore():
    if HLA_SCORE["DR"] >= 2:
        return 0
    return (2 - HLA_SCORE["DR"]) / 2


def getDQScore():
    if HLA_SCORE["DQ"] >= 2:
        return 0
    return (2 - HLA_SCORE["DQ"]) / 2


def getAgeMalus(receiver: Person):
    if receiver.age <= 45:
        return 1
    elif receiver.age > 75:
        return 0
    return (75 - receiver.age) / 30


def getAgeBonus(receiver: Person):
    if receiver.age < 45:
        return 0
    elif receiver.age >= 100:
        return 1
    return (100 - receiver.age) / 55


def getFagScore():
    return 0
