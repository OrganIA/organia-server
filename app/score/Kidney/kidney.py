#from _typeshed import Self
#from _typeshed import IdentityFunction
from logging import Handler, info
from sqlalchemy.sql.elements import Null
from datetime import date
import math
import json
from DialyseScore import DialyseScore
import Other
#https://www.agence-biomedecine.fr/IMG/pdf/guide_score_rein_v1.pdf

class Score_HAge:
    def __init__(self, Info):
        self.DS = DialyseScore(Info)
        self.HLA =  Other.HlaScore(Info)
        self.AGE = Other.AgeScore(Info)
    
   # Score = 100 * DD + 200 * f2(DA, DD) + [100 x f3(A,B) + 400 x f4(DR) + 100 x f4(DQ) + 150 x f7(FAG)] x f5(AgeR, 45, 75) + 750 x f6(AgeR, 45, 100)
    def getHAge(self):
        return 100 * self.DS.getScore() + 200 * self.DS.getWaitingScore() + (100 * self.HLA.getAbScore() + 400 * self.HLA.getDrScore() + 100 * self.HLA.getDqScore() + 150 * self.HLA.getFagScore() * self.AGE.getAgeMalus() + 750 * self.AGE.getAgeBonus())

class DifferentialAge:
    def __init__(self, Info):
        self.ageR = Info.ageR
        self.ageD = Info.ageD

    def checkAge(self):
        if self.ageR - self.ageD > 5:
            return 100
        else:
            return abs(self.ageR - self.ageD)

    def getDifferentialAge(self):
        age = self.checkAge()
        return 1 / (math.exp(pow(0.02 * age, 0.85)))

class KidneyScoring:
    def __init__(self):
        self.AllInfo = Other.Info
        self.HAge = Score_HAge(self.AllInfo).getHAge()
        self.FAge = DifferentialAge(self.AllInfo).getDifferentialAge()

    def getScoreHD(self):
        if self.AllInfo.ageR > (self.AllInfo.ageD + 20):
            check = 0
        else:
            check = 1
        return (self.HAge * check) / self.FAge

def main():
    KidneyScoringClass = KidneyScoring()
    score = KidneyScoringClass.getScoreHD()
    print(score)

if __name__ == "__main__":
    main()

