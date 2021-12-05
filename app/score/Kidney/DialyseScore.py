from datetime import date
from sqlalchemy.sql.elements import Null
from Other import Info

class DialyseScore:
    def __init__(self, Info):
        self.isDialyse = Info.isDialyse
        self.isRetransplantation = Info.isRetransplantation
        self.DateStartDialyse = Info.DateStartDialyse
        self.DateReturnDialyse = Info.DateReturnDialyse
        self.DateInscription =  Info.DateInscription
        self.DateGreffe = Info.DateGreffe
        self.DateArf = Info.DateArf

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
