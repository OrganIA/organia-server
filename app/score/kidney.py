#from _typeshed import Self
#from _typeshed import IdentityFunction
from logging import Handler
from sqlalchemy.sql.elements import Null
from datetime import date
import math
import json
#https://www.agence-biomedecine.fr/IMG/pdf/guide_score_rein_v1.pdf

class AgeScore:
    age = 45
    @classmethod
    def getAgeMalus(self):
        if (self.age <= 45):
            return 1
        if (self.age > 75):
            return 0
        return (75 - self.age) / 30
    @classmethod
    def getAgeBonus(self):
        if (self.age < 45):
            return 0
        if (self.age >= 100):
            return 1
        return (100 - self.age) / 55
    @classmethod
    def getAge(self):
        return self.age

#HLA-A, B, DR 4 400 (35 %) 400 x (1-nombre d’incompatibilités HLA/6)
#Probabilité d’incompatibilité 1 100 (8 %) 100 x (1-[ABO[1] x (1-[% anticorps anti-HLA/100]) x (INCp0[2] + INCp1)])1 000
class HlaScore: #human leucocyte antigen incompatibilité
    A = 0
    B = 0
    DR = 0
    DQ = 0

    @classmethod
    def getAbScore(self):
        x = self.A + self.B
        if (x >= 4):
            return 0
        return (4 - x) / 4
    @classmethod
    def getDrScore(self):
        if (self.DR >= 2):
            return 0
        return (2- self.DR) / 2
    @classmethod
    def getDqScore(self):
        if (self.DQ >= 2):
            return 0
        return (2 - self.DQ) / 2
    @classmethod #basé sur la rareté du score Hla
    def getFagScore(self):
        return 0

#La date de Début de dialyse (en cours) est définie comme la date de début du traitement de
#suppleance en cours au moment de la saisie.
#Pour les patients en attente d’une retransplantation, la date de Début de dialyse correspond à la
#Date de retour en dialyse (qui est également la date d’arrêt fonctionnel du greffon).
class DialyseScore:
    isDialyse = True #https://www.fondation-du-rein.org/quest-ce-que-la-dialyse/
    isRetransplantation = False #first time or not
    DateStartDialyse = date(2021, 10, 1) #n
    DateReturnDialyse = date(2019, 5, 5) #n - 1
    DateInscription =  date(2019, 5, 5)
    DateGreffe = Null
    DateArf = Null #Arrêt fonctionnel du greffon

    @classmethod
    def getDate(self):
        if self.isDialyse == False:
            return 0
        #
        if self.isRetransplantation == False:
            if self.DateStartDialyse != Null:
                return self.DateStartDialyse
            else:
                return 0
        #
        if self.DateReturnDialyse != Null & self.DateReturnDialyse > self.DateGreffe:
            return self.DateReturnDialyse
        #
        if self.DateArf != Null:
            return self.DateArf
        else: return self.DateStartDialyse
    @classmethod
    def getScore(self):
        try:
            s = (date.today() - self.getDate()).days
            if s > 3650:
                return 1
            if s < 0:
                print("Error: Date invalid")
                return 0
            return s / 3650
        except:
            return 0
    @classmethod
    def getWaitingTime(self):
        if self.isRetransplantation or (self.DateInscription - self.DateStartDialyse) < 360:
            return self.DateInscription
        if self.isRetransplantation == False and (self.DateInscription - self.DateStartDialyse) >= 360:
            return 12 + self.DateStartDialyse
        return -1 #need to check error
    @classmethod
    def getWaitingScore(self):
        if self.getWaitingTime() >= 3600:
            return 1
        else:
            return 1 / 120 * self.getWaitingTime()

class Score_HAge:
    DS = DialyseScore()
    HLA =  HlaScore()
    AGE = AgeScore()
    isIdf = True
    distance = 60
   # Score = 100 * DD + 200 * f2(DA, DD) + [100 x f3(A,B) + 400 x f4(DR) + 100 x f4(DQ) + 150 x f7(FAG)] x f5(AgeR, 45, 75) + 750 x f6(AgeR, 45, 100)
    @classmethod
    def getWithoutAgeScore(self):
        return 100 * self.DS.getScore() + 200 * self.DS.getScore() + (100 * self.HLA.getAbScore() + 400 * self.HLA.getDrScore() + 100 * self.HLA.getDqScore() + 150 * self.HLA.getFagScore() * self.AGE.getAgeMalus() + 750 * self.AGE.getAgeBonus())
    @classmethod
    def getWithAgeScore(self, AgeD):
        x = 0
        y = 0
        if self.AGE.age > (AgeD + 20):
            x = 0
        else:
            x = self.getScore()
        if self.AGE.age > AgeD + 5:
            y = 100
        else:
            y = abs(self.AGE.age - AgeD)
        y = math.exp(0.02 * y ** 0.85)
        return x / y
    @classmethod
    def getNationalScore(self, isIdf, distance, AgeD): # distance = valeur en minute entre le donneur et le reçeveur
        if self.isIdf & isIdf:
            return self.getWithAgeScore(AgeD)
        return (1/math.exp(0.0000002 * distance ** 2.9)) * self.getWithAgeScore(AgeD)

class DifferentialAge:
    def __init__(self, AgeR, AgeD):
        self.AgeR = AgeR
        self.AgeD = AgeD
    def checkAge(self):
        if self.AgeR - self.AgeD > 5:
            return 100
        else:
            return abs(self.AgeR - self.AgeD)

    def getDifferentialAge(self):
        age = self.checkAge()
        return 1 / (math.exp(pow(0.02 * age, 0.85)))

class ScoreHD:
    def __init__(self, AgeR, AgeD):
        self.AgeR = AgeR
        self.AgeD = AgeD
        self.HAge = Score_HAge().getWithoutAgeScore()
        self.FAge = DifferentialAge(AgeR, AgeD).getDifferentialAge()

    def getScoreHD(self):
        if self.AgeR > (self.AgeD + 20):
            check = 0
        else:
            check = 1
        return (self.HAge * check) / self.FAge

def main():
   test = DialyseScore
   test2 = ScoreHD(25, 30).getScoreHD()
   print(test2)
#    print(test.getScore())
#    f = open ('data.json', "r")
#    data = json.loads(f.read())

if __name__ == "__main__":
   main()

