from datetime import date

from pydantic import BaseModel

from app import db
from app.api.person import get_person
from app.db.models import Kidney, Listing
from app.errors import InvalidRequest, NotFoundError
from app.score.kidney.kidney_score import compute_kidney_score
from app.utils.bp import Blueprint

bp = Blueprint(__name__)


class KidneySchema(BaseModel):
    is_dialyse: bool
    is_retransplantation: bool
    start_date_dialyse: date
    arf_date: date
    date_transplantation: date
    re_registration_date: date


async def compute_matches_kidney(listing_id: int):
    donor_listing = (
        db.session.query(Listing).filter(listing_id == Listing.id).first()
    )
    if donor_listing is None:
        raise NotFoundError(
            'Id provided doest not refer to an existing listing'
        )
    if donor_listing.type == Listing.Type.RECEIVER:
        raise InvalidRequest('This listing is a receiver not a donor')
    receivers_listings = (
        db.session.query(Listing)
        .filter(
            Listing.id != listing_id,
            Listing.type == Listing.Type.RECEIVER,
            Listing.organ == Listing.Organ.KIDNEY,
        )
        .all()
    )
    donor_person = await get_person(listing_id)

    result_listing = []
    for receiver in receivers_listings:
        receiver_person = await get_person(receiver.person_id)
        result_listing.append(
            [
                receiver,
                compute_kidney_score(receiver_person, donor_person, receiver),
            ]
        )
        return result_listing
