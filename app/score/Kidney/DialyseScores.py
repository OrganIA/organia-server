import datetime


def getDate(receiver_listing):
    if receiver_listing.isDialyse is False:
        return 0
    elif receiver_listing.isRetransplantation is False:
        if receiver_listing.startDateDialyse is not None:
            return (receiver_listing.prelDate - receiver_listing.startDateDialyse).days / 365.25
        else:
            return 0
    elif receiver_listing.DialyseReturnDate is not None and receiver_listing \
            .DialyseReturnDate > receiver_listing.transplantationDate:
        return (receiver_listing.prelDate - receiver_listing.DialyseReturnDate).days / 365.25
    elif receiver_listing.ARFDate is not None:
        return receiver_listing.ARFDate
    else:
        return receiver_listing.InscriptionDate


def getScore(receiver_listing):
    date = getDate(receiver_listing)
    if date >= 10:
        return 1
    else:
        return date / 10

def getWaitingTime(receiver_listing):
    inscription_date = receiver_listing.ResumptionDateSeniority if receiver_listing.ResumptionSeniority == 'O' else receiver_listing.InscriptionDate
    DATT = (receiver_listing.prelDate - inscription_date).days / 365
    if receiver_listing.isDialyse:
        DDIAL = (receiver_listing.prelDate - receiver_listing.startDateDialyse).days / 365
    else:
        DDIAL = 0
    if receiver_listing.isRetransplantation is True or (DATT - DDIAL) < 1:
        return DATT
    elif receiver_listing.isRetransplantation is False and (DATT - DDIAL) >= 1:
        return 1 + DDIAL
    return -1  # need to check error


def getWaitingScore(receiver_listing):
    res = getWaitingTime(receiver_listing)
    if res >= 10:
        return 1
    else:
        return res / 10
