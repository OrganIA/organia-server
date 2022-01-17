import math
# from app.models import Person, Listing
from app.score.Kidney.HLA_Age import getABScore, getAgeBonus, getAgeMalus, getDQScore, getDRScore, getFagScore
from app.score.Kidney.DialyseScores import getScore, getWaitingScore


def getHAge(receiver, receiver_listing):
    return 100 * getScore(receiver_listing) + 200 * getWaitingScore(receiver_listing) + (100 * getABScore(receiver_listing) + 400 * getDRScore(receiver_listing) + 100 * getDQScore(receiver_listing) + 150 * getFagScore()) * getAgeMalus(receiver) + 750 * getAgeBonus(receiver)


def checkAge(receiver, donor):
    if receiver["age"] - donor["age"] > 5:
        return 100
    else:
        return abs(receiver - donor)


def getDifferentialAge(receiver, donor):
    age = checkAge(receiver, donor)
    return 1 / (math.exp(pow(0.02 * age, 0.85)))


def getScoreHD(receiver, donor, receiver_listing):
    HAge = getHAge(receiver, receiver_listing)
    FAge = getDifferentialAge(receiver, donor)
    if receiver.age > donor.age + 20:
        check = 0
    else:
        check = 1
    return (HAge * check) / FAge

def getScoreNAP(receiver, donor, receiver_listing):
    ScoreHD = getScoreHD(receiver, donor, receiver_listing)
    MGScore = 0

    return ScoreHD * MGScore
