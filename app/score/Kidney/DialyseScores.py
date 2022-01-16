from datetime import date
from Other import Info
from app.models import Person, Listing


def getDate(receiver_listing: Listing):
    if receiver_listing.isDialyse is False:
        return 0
    elif receiver_listing.isRetransplantation is False:
        if receiver_listing.startDateDialyse is None:
            return receiver_listing.startDateDialyse
        else:
            return 0
    elif receiver_listing.EndDateDialyse is None and receiver_listing.EndDateDialyse > receiver_listing.DateTransplantation:
        return receiver_listing.EndDateDialyse
    elif receiver_listing.ARFDate is not None:
        return receiver_listing.ARFDates
    else:
        return receiver_listing.startDateDialyse


def getScore(receiver_listing: Listing):
    try:
        s = (date.today() - getDate(receiver_listing)).days
        if s > 3650:
            return 1
        elif s < 0:
            print("Error: Date invalid")
            return 0
        return s / 3650
    except:
        return 0


def getWaitingTime(receiver_listing: Listing):
    DATT = date.today() - receiver_listing.DateInscription
    if receiver_listing.isDialyse:
        DDIAL = date.today() - receiver_listing.startDateDialyse
    else:
        DDIAL = 0
    if receiver_listing.isRetransplantation or (DATT - DDIAL).days < 365:
            return DATT
    elif receiver_listing.isRetransplantation == False and (receiver_listing.DateInscription - receiver_listing.DateStartDialyse) >= 365:
        return 12 + DDIAL
    return -1 #need to check error


def getWaitingScore(receiver_listing: Listing):
        if getWaitingTime().days >= 3600:
            return 1
        else:
            return (1 / 120) * getWaitingTime().days