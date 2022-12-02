from datetime import datetime

from app import db
from app.db.models import Listing, Liver
from app.errors import NotFoundError
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint('listings', auth=True)


class ListingSchema(Static):
    @staticmethod
    def dialysis_start_date(d):
        dialysis_start_date = Static._get(d, 'dialysis_start_date')
        return datetime.fromisoformat(dialysis_start_date).date()

    @staticmethod
    def dialysis_end_date(d):
        dialysis_end_date = Static._get(d, 'dialysis_end_date')
        return datetime.fromisoformat(dialysis_end_date).date()

    @staticmethod
    def arf_date(d):
        arf_date = Static._get(d, 'arf_date')
        return datetime.fromisoformat(arf_date).date()

    @staticmethod
    def transplantation_date(d):
        transplantation_date = Static._get(d, 'transplantation_date')
        return datetime.fromisoformat(transplantation_date).date()

    @staticmethod
    def re_registration_date(d):
        re_registration_date = Static._get(d, 're_registration_date')
        return datetime.fromisoformat(re_registration_date).date()

    notes = str
    type = Listing.Type
    organ = Listing.Organ
    tumors_number = int
    biggest_tumor_size = int
    alpha_fetoprotein = int
    is_under_dialysis = bool
    A = int
    B = int
    DR = int
    DQ = int
    person_id = int
    hospital_id = int


def create_organ(data):
    # Update this function when an organ is implemented
    listing = db.session.query(Listing).order_by(Listing.id.desc()).first()
    organ = {}
    if listing.organ.value == "LIVER":
        organ = Liver()
        organ = update(organ, data)
    organ.listing_id = listing.id
    organ.score = 0.0
    return organ


def update(listing, data):
    for key, value in data.dict.items():
        if value == 'null':
            setattr(listing, key, None)
        elif value is not None:
            setattr(listing, key, value)
    return listing


@bp.get('/')
def get_listings():
    return db.session.query(Listing)


@bp.get('/<int:id>')
def get_listing(id):
    result = db.session.get(Listing, id)
    if not result:
        raise NotFoundError
    return result


@bp.post('/')
def create_listing(data: ListingSchema):
    listing = Listing(**data.dict)
    db.session.add(listing)
    db.session.commit()
    create_organ(data)
    return get_listing(listing.id)


@bp.post('/<int:id>')
def update_listing(id, data: ListingSchema):
    listing = db.session.get(Listing, id)
    db.session.commit()
    return update(listing, data)


@bp.delete('/<int:id>')
def delete_listing(id: int):
    listing = get_listing(id)
    db.session.delete(listing)
    db.session.commit()


@bp.get('/<int:id>/matches')
def get_listing_matches(id):
    import random

    def schemaify(l: Listing):
        return {
            'id': l.id,
            'type': l.type,
            'notes': l.notes,
            'organ': l.organ,
            'person_id': l.person_id,
            'hospital_id': l.hospital_id,
        }

    return sorted(
        [
            {
                "listing": schemaify(l),
                "score": random.random(),
            }
            for l in db.session.query(Listing)
        ],
        key=lambda x: x['score'],
        reverse=True,
    )
