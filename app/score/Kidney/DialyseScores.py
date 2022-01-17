from datetime import date
from app.models import Person, Listing


def getDate(receiver_listing: Listing):
    if receiver_listing.dialyse is False:
        return 0
    elif receiver_listing.retransplantation is False:
        if receiver_listing.start_date_dialyse is not None:
            return receiver_listing.start_date_dialyse
        else:
            return 0
    elif receiver_listing.end_date_dialyse is not None and receiver_listing.end_date_dialyse > receiver_listing.transplantation_date:
        return receiver_listing.end_date_dialyse
    elif receiver_listing.arf_date is not None:
        return receiver_listing.arf_date
    else:
        return receiver_listing.second_registration_date


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
    DATT = date.today() - receiver_listing.startDateDialyse
    if receiver_listing.isDialyse:
        DDIAL = date.today() - receiver_listing.startDateDialyse
    else:
        DDIAL = 0
    if receiver_listing.isRetransplantation or (DATT - DDIAL).days < 365:
        return DATT
    elif receiver_listing.isRetransplantation is False and (receiver_listing.start_date - receiver_listing.startDateDialyse) >= 365:
        return 12 + DDIAL
    return -1  # need to check error


def getWaitingScore(receiver_listing: Listing):
    if getWaitingTime(receiver_listing).days >= 3650:
        return 1
    else:
        return (1 / 120) * getWaitingTime(receiver_listing).days
