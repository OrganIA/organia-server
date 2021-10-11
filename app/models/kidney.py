#from _typeshed import Self
from sqlalchemy.sql.elements import Null
from datetime import date


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


class FagScore: #Besoin de la base de donnée -> basé sur la rareté du score Hla
    @classmethod
    def getFagScore(self):
        return 0
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
    def getDrScore(self):
        if (self.DR >= 2):
            return 0
        return (2- self.DR) / 2
    def getDqScore(self):
        if (self.DQ >= 2):
            return 0
        return (2 - self.DQ) / 2



class DialyseScore:
    isDialyse = True#https://www.fondation-du-rein.org/quest-ce-que-la-dialyse/
    isRetransplantation = False #first time or not
    DateNewDialyse = date(2021, 10, 1) #n
    DateOldDialyse = date(2019, 5, 5) #n - 1
    DateGreffe = Null
    DateArf = Null #Arrêt fonctionnel du greffon

    @classmethod
    def getDate(self):
        if self.isDialyse == False:
            return 0
        #
        if self.isRetransplantation == False:
            if self.DateNewDialyse != Null:
                return self.DateNewDialyse
            else:
                return 0
        #
        if self.DateOldDialyse != Null & self.DateOldDialyse > self.Greffe:
            return self.DateOldDialyse
        #
        if self.DateArf != Null:
            return self.DateArf
        else: return self.DateNewDialyse
    @classmethod
    def getScore(self):
        try:
            s = (date.today() - self.getDate()).days
            if s > 3650:
                return 1
            if s < 0:
                print("Error: Date invalid")
                return 0
            print(s)
            return s / 3650
        except:
            return 0
    @classmethod
    def getWaitingTime(self):
        

class Score_HAge:
    DS = DialyseScore()
    HLA =  HlaScore()
    FAG = FagScore()
    AGE = AgeScore()
    ageDonneur = 30
   # Score = 100 * DD + 200 * f2(DA, DD) + [100 x f3(A,B) + 400 x f4(DR) + 100 x f4(DQ) + 150 x f7(FAG)] x f5(AgeR, 45, 75) + 750 x f6(AgeR, 45, 100)
    @classmethod
    def getScore(self):
        return 100 * self.DS.getScore() + 200 * self.DS.getScore() + (100 * self.HLA.getAbScore() + 400 * self.HLA.getDrScore + 100 * self.HLA.getDqScore + 150 * self.FAG.getFagScore) * self.AGE.getAgeMalus() + 750 * self.AGE.getAgeBonus()

#def main():
#    test = DialyseScore
#    print(test.getScore())

#if __name__ == "__main__":
#    main()

