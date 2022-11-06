import datetime
from app.models import Listing, Kidney


def getDate(receiver_listing: Listing, listing_kidney):
    if listing_kidney.isDialyse is False:
        return 0
    elif listing_kidney.isRetransplantation is False:
        if listing_kidney.startDateDialyse is not None:
            return listing_kidney.startDateDialyse
        else:
            return 0
    elif listing_kidney.EndDateDialyse is not None and listing_kidney\
        .EndDateDialyse > listing_kidney.DateTransplantation:
        return listing_kidney.EndDateDialyse
    elif listing_kidney.ARFDate is not None:
        return listing_kidney.ARFDate
    else:
        return listing_kidney.ReRegistrationDate


def getScore(receiver_listing: Listing, listing_kidney):
    try:
        s = (datetime.datetime.today() - getDate(receiver_listing, listing_kidney)).days
        if s > 3650:
            return 1
        elif s < 0:
            print("Error: Date invalid")
            return 0
        return s / 3650
    except:
        return 0


def getWaitingTime(receiver_listing: Listing, listing_kidney):
    #A revoir
    DATT = datetime.date.today() - listing_kidney.startDateDialyse
    if listing_kidney.isDialyse:
        DDIAL = datetime.date.today() - listing_kidney.startDateDialyse
    else:
        DDIAL = 0
    if listing_kidney.isRetransplantation or (DATT - DDIAL).days < 365:
        return DATT
    elif listing_kidney.isRetransplantation is False and (listing_kidney.\
        startDateDialyse - listing_kidney.startDateDialyse) >= 365:
        return 12 + DDIAL
    return -1  # need to check error


def getWaitingScore(receiver_listing: Listing, listing_kidney):
    #A revoir
    if getWaitingTime(receiver_listing, listing_kidney).days >= 3650:
        return 1
    else:
        return (1 / 120) * getWaitingTime(receiver_listing, listing_kidney).days
