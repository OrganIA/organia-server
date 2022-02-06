import datetime
from app.models import Listing


def getDate(receiver_listing: Listing):
    if receiver_listing.isDialyse is False:
        return 0
    elif receiver_listing.isRetransplantation is False:
        if receiver_listing.startDateDialyse is not None:
            return receiver_listing.startDateDialyse
        else:
            return 0
    elif receiver_listing.EndDateDialyse is not None and receiver_listing\
        .end_date_dialyse > receiver_listing.transplantation_date:
        return receiver_listing.EndDateDialyse
    elif receiver_listing.ARFDate is not None:
        return receiver_listing.ARFDate
    else:
        return receiver_listing.ReRegistrationDate


def getScore(receiver_listing: Listing):
    try:
        s = (datetime.datetime.today() - getDate(receiver_listing)).days
        if s > 3650:
            return 1
        elif s < 0:
            print("Error: Date invalid")
            return 0
        return s / 3650
    except:
        return 0


def getWaitingTime(receiver_listing: Listing):
    DATT = datetime.date.today() - receiver_listing.startDateDialyse
    if receiver_listing.isDialyse:
        DDIAL = datetime.date.today() - receiver_listing.startDateDialyse
    else:
        DDIAL = 0
    if receiver_listing.isRetransplantation or (DATT - DDIAL).days < 365:
        return DATT
    elif receiver_listing.isRetransplantation is False and (receiver_listing.\
        startDateDialyse - receiver_listing.startDateDialyse) >= 365:
        return 12 + DDIAL
    return -1  # need to check error


def getWaitingScore(receiver_listing: Listing):
    if getWaitingTime(receiver_listing).days >= 3650:
        return 1
    else:
        return (1 / 120) * getWaitingTime(receiver_listing).days
