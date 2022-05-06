from math import sqrt, exp
from cmath import isnan
from app.distance import get_distance
from app.score.Kidney.HLA_Age import (
    getABScore,
    getAgeBonus,
    getAgeMalus,
    getDQScore,
    getDRScore,
)
from app.score.Kidney.DialyseScores import getScore, getWaitingScore

from test import sample1


class Receiver:
    def __init__(self, data):
        self.age = (data['D_D_PREL'] - data['R_D_NAI']).days / 365


class Donor:
    def __init__(self, data):
        self.age = (data['D_D_PREL'] - data['D_D_NAI']).days / 365


class ReceiverListing:
    def __init__(self, data):
        self.prelDate = data['D_D_PREL']
        self.FAG = 1 - data['FAG'] / data['MAXFAG']
        self.isDialyse = False if isnan(data['D_DIAL'].day) else True
        self.isRetransplantation = False if isnan(data['D_Ret_DIAL (n-1)'].day) else True
        self.DialyseReturnDate = data['D_Ret_DIAL (n-1)']
        self.InscriptionDate = data['R_D_INSC']
        self.startDateDialyse = data['D_DIAL']
        self.ResumptionSeniority = data['Reprise_ANC']
        self.ResumptionDateSeniority = data['D_Reprise_ANC']
        self.ARFDate = data['D_ARF (n-1)']
        self.transplantationDate = data['D_GRF (n-1)']

        self.A = data['Incomp_A']
        self.B = data['Incomp_B']
        self.DR = data['Incomp_DR']
        self.DQ = data['Incomp_DQ']


class MG:
    def __init__(self, data):
        self.Alea = data['Alea']
        self.ZoneDON = data['ZoneDON']
        self.ZoneREC = data['ZoneREC']
        self.Distance = data['DISTANCE']
        self.Kequipe = data['Kequipe']


def getHAge(receiver, receiver_listing):
    print(getWaitingScore(receiver_listing))
    return 100 * getScore(receiver_listing) \
           + 200 * getWaitingScore(receiver_listing) \
           + (100 * getABScore(receiver_listing) \
              + 400 * getDRScore(receiver_listing) \
              + 100 * getDQScore(receiver_listing) \
              + 150 * receiver_listing.FAG) * getAgeMalus(receiver) \
           + 750 * getAgeBonus(receiver)


def checkAge(receiver, donor):
    if receiver.age - donor.age > 5:
        return 100
    else:
        return abs(receiver.age - donor.age)

def getScoreHD(receiver, donor, receiver_listing):
    HAge = getHAge(receiver, receiver_listing)
    FAge = checkAge(receiver, donor)
    print(HAge, FAge)
    if receiver.age > donor.age + 20:
        check = 0
    else:
        check = 1
    return (HAge * check) / (exp(0.02 * pow(FAge, 0.85)))


def getScoreMG(MG):
    if MG.ZoneREC == "HORS_IDF":
        if (MG.Distance / sqrt(MG.Kequipe)) <= (150 / (100 / 60)):
            return 1 - (MG.Distance / sqrt(MG.Kequipe) / (3000 / (100 / 60)))
        elif (MG.Distance / sqrt(MG.Kequipe)) <= (500 / (100 / 60)):
            return 0.95 - (MG.Distance / sqrt(MG.Kequipe) - (150 / (100 / 60))) / (830 / (100 / 60))
        elif MG.Distance / sqrt(MG.Kequipe) <= (2000 / (100 / 60)):
            return 0.5 - (MG.Distance / sqrt(MG.Kequipe) - (525 / (100 / 60))) / (3000 / (100 / 60))
        else:
            return 0
    elif MG.Alea < 0.2 or MG.ZoneDON == "IDF":
        return 1
    else:
        return 0


# def getScoreMG(hospital_1, hospital_2):
#   MG = get_distance(hospital_1, hospital_2)
#  return MG


def getScoreNAP(receiver, donor, receiver_listing, mg):
    ScoreHD = getScoreHD(receiver, donor, receiver_listing)
    MGScore = getScoreMG(mg)
    #MGScore = getScoreMG("MARSEILLE", "PARIS")
    print(ScoreHD, MGScore)
    return ScoreHD * MGScore


receiver = Receiver(sample1)
donor = Donor(sample1)
receiver_listing = ReceiverListing(sample1)
mg = MG(sample1)

NAP = getScoreNAP(receiver, donor, receiver_listing, mg)
print(NAP)
