import math

from app.models import Person
from app.score.Kidney.HLA_Age import *
from app.score.Kidney.DialyseScores import *


def getHAge(receiver: Person, receiver_listing: Listing):
    return 100 * getScore(receiver_listing) + 200 * getWaitingScore(receiver_listing) + (100 * getABScore() + 400 * getDRScore() + 100 * getDQScore() + 150 * getFagScore( * getAgeMalus(receiver) + 750 * getAgeBonus(receiver)))


def checkAge(receiver: Person, donor: Person):
    if receiver.age - donor.age > 5:
        return 100
    else:
        return abs(receiver.age - donor.age)


def getDifferentialAge(receiver: Person, donor: Person):
    age = checkAge(receiver, donor)
    return 1 / (math.exp(pow(0.02 * age, 0.85)))


def getScoreHD(receiver: Person, donor: Person, receiver_listing: Listing):
    HAge = getHAge(receiver, receiver_listing)
    FAge = getDifferentialAge(receiver, donor)
    if receiver.age > donor.age + 20:
        check = 0
    else:
        check = 1
    return (HAge * check) / FAge