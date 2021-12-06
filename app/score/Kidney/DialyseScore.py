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
        self.CurrentDate = Info.CurrentDate

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
    
    def getWaitingTime(self):
        DATT = self.CurrentDate - self.DateInscription
        if self.isDialyse:
            DDIAL = self.CurrentDate - self.DateStartDialyse
        else:
            DDIAL = 0
        if self.isRetransplantation or (DATT - DDIAL).days < 365:
            return DATT
        elif self.isRetransplantation == False and (self.DateInscription - self.DateStartDialyse) >= 365:
            return 12 + DDIAL
        return -1 #need to check error
    
    def getWaitingScore(self):
        if self.getWaitingTime().days >= 3600:
            return 1
        else:
            return (1 / 120) * self.getWaitingTime().days
