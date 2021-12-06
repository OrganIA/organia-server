from datetime import date
from sqlalchemy.sql.elements import Null

class Info:

    # DialyseScore
    isDialyse = True #https://www.fondation-du-rein.org/quest-ce-que-la-dialyse/
    isRetransplantation = False #first time or not
    DateStartDialyse = date(2019, 10, 1) #n
    DateReturnDialyse = date(2021, 11, 5) #n - 1
    DateInscription =  date(2019, 5, 5)
    CurrentDate = date(2021, 10, 21)
    DateGreffe = Null
    DateArf = Null #Arrêt fonctionnel du greffon

    # HlaScore
    A = 0
    B = 0
    DR = 0
    DQ = 0

    # AgeScore
    ageR = 25
    ageD = 45


class AgeScore:

    def __init__(self, Info):
        self.ageR = Info.ageR
    
    def getAgeMalus(self):
        if (self.ageR <= 45):
            return 1
        if (self.ageR > 75):
            return 0
        return (75 - self.age) / 30
    
    def getAgeBonus(self):
        if (self.ageR < 45):
            return 0
        if (self.ageR >= 100):
            return 1
        return (100 - self.ageR) / 55
    
    def getAge(self):
        return self.ageR


#HLA-A, B, DR 4 400 (35 %) 400 x (1-nombre d’incompatibilités HLA/6)
#Probabilité d’incompatibilité 1 100 (8 %) 100 x (1-[ABO[1] x (1-[% anticorps anti-HLA/100]) x (INCp0[2] + INCp1)])1 000
class HlaScore: #human leucocyte antigen incompatibilité
    def __init__(self, Info):
        self.A = Info.A
        self.B = Info.B
        self.DR = Info.DR
        self.DQ = Info.DQ

    def getAbScore(self):
        x = self.A + self.B
        if (x >= 4):
            return 0
        return (4 - x) / 4

    def getDrScore(self):
        if (self.DR >= 2):
            return 0
        return (2- self.DR) / 2

    def getDqScore(self):
        if (self.DQ >= 2):
            return 0
        return (2 - self.DQ) / 2

    def getFagScore(self):
        return 0