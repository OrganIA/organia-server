


#from _typeshed import Self
from sqlalchemy.sql.elements import Null
from datetime import date

#class HlaScore: #human leucocyte antigen incompatibilité
#    A = 0
#    B = 0
#    DR = 0
#    DQ = 0

#    @classmethod
#    def getAbScore(self):


class DialyseScore:
    isDialyse = True#https://www.fondation-du-rein.org/quest-ce-que-la-dialyse/ -> diabète du rein
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
class Score_HAge:
    DD = 0

#def main():
#    test = DialyseScore
#    print(test.getScore())

#if __name__ == "__main__":
#    main()

