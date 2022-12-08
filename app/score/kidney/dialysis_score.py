import datetime

from app.db.models import Listing


def get_date(listing_kidney):
    if not listing_kidney.is_under_dialysis:
        return 0
    elif not listing_kidney.is_retransplantation:
        if listing_kidney.dialysis_start_date is not None:
            return listing_kidney.dialysis_start_date
        else:
            return 0
    elif (
        listing_kidney.dialysis_end_date is not None
        and listing_kidney.dialysis_end_date
        > listing_kidney.date_transplantation
    ):
        return listing_kidney.dialysis_end_date
    elif listing_kidney.arf_date is not None:
        return listing_kidney.arf_date
    else:
        return listing_kidney.re_registration_date


def get_score(receiver_listing: Listing, listing_kidney):
    try:
        s = (
            datetime.datetime.today()
            - get_date(receiver_listing, listing_kidney)
        ).days
        if s > 3650:
            return 1
        elif s < 0:
            print("Error: Date invalid")
            return 0
        return s / 3650
    except Exception:
        return 0


def get_waiting_time(listing_kidney):
    # A revoir
    DATT = datetime.date.today() - listing_kidney.dialysis_start_date
    if listing_kidney.is_under_dialysis:
        DDIAL = datetime.date.today() - listing_kidney.dialysis_start_date
    else:
        DDIAL = 0
    if listing_kidney.is_retransplantation or (DATT - DDIAL).days < 365:
        return DATT
    elif (
        not listing_kidney.is_retransplantation
        and (
            listing_kidney.dialysis_start_date
            - listing_kidney.dialysis_start_date
        )
        >= 365
    ):
        return 12 + DDIAL
    return -1  # need to check error


def get_waiting_score(receiver_listing: Listing, listing_kidney):
    # A revoir
    # if get_waiting_time(receiver_listing, listing_kidney).days >= 3650:
    if get_waiting_time(listing_kidney).days >= 3650:
        return 1
    else:
        # return (1 / 120) * get_waiting_time(
        #     receiver_listing, listing_kidney
        # ).days
        return (1 / 120) * get_waiting_time(listing_kidney).days
