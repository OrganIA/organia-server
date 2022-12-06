from datetime import date

import flask
from pydantic import BaseModel

from app import db
from app.api.lungs import LungSchema, compute_matches
from app.api.person import PersonSchema
from app.db.models import Heart, Listing, Liver, Lung
from app.db.models.person import Person
from app.errors import InvalidRequest, NotFoundError
from app.utils.bp import Blueprint

bp = Blueprint(__name__)


class ListingSchema(BaseModel):
    hospital_id: int
    notes: str
    organ: Listing.Organ
    person_id: int
    type: Listing.Type

    is_under_dialysis: bool
    re_registration_date: date
    transplantation_date: date
    dialysis_end_date: date
    dialysis_start_date: date
    alpha_fetoprotein: int
    arf_date: date
    biggest_tumor_size: int
    tumors_number: int
    A: int
    B: int
    DQ: int
    DR: int

    lung: LungSchema
    person: PersonSchema


def update_organ(data, id):
    organ = {}
    if data.organ == Listing.Organ.LIVER:
        organ = db.session.query(Liver).filter_by(listing_id=id).first()
        organ = update(organ, data)
        db.session.commit()
    if data.organ == Listing.Organ.LUNG:
        organ = db.session.query(Lung).filter_by(listing_id=id).first()
        print("ORGAN: ", organ)
        organ = update(organ, data)
        db.session.commit()
    return organ


def update(listing, data):
    for key, value in data.dict().items():
        if value == 'null':
            setattr(listing, key, None)
        elif value is not None:
            setattr(listing, key, value)
    return listing


@bp.get('/')
def get_listings():
    query = db.session.query(Listing)
    if type := flask.request.args.get('type'):
        try:
            type = Listing.Type(type.upper())
        except ValueError:
            raise InvalidRequest(f'Invalid type {type}')
        query = query.filter_by(type=type)
    return query


@bp.get('/organs')
def get_organs():
    return Listing.Organ.values()


@bp.get('/<int:id>')
def get_listing(id):
    result = db.session.get(Listing, id)
    if not result:
        raise NotFoundError
    return result


@bp.post('/')
def create_listing(data: ListingSchema):
    data = data.dict()
    liver_data = data.pop("liver", None)
    lung_data = data.pop("lung", None)
    heart_data = data.pop("heart", None)
    person_data = data.pop("person", None)
    if liver_data:
        data["liver"] = Liver(**liver_data)
    if lung_data:
        data["lung"] = Lung(**lung_data)
    if heart_data:
        data["heart"] = Heart(**heart_data)
    if person_data:
        data["person"] = Person(**person_data)
    listing = Listing(**data)
    db.session.add(listing)
    db.session.commit()
    return get_listing(listing.id)


@bp.post('/<int:id>')
def update_listing(id, data: ListingSchema):
    listing = db.session.get(Listing, id)
    if not listing:
        raise NotFoundError
    listing = update(listing, data)
    update_organ(data, id)
    db.session.commit()
    return listing


@bp.delete('/<int:id>')
def delete_listing(id: int):
    listing = get_listing(id)
    db.session.delete(listing)
    db.session.commit()


@bp.get('/<int:id>/matches')
def get_listing_matches(id):
    def schemaify(listing: Listing):
        return {
            'id': listing.id,
            'type': listing.type,
            'notes': listing.notes,
            'organ': listing.organ,
            'person_id': listing.person_id,
            'hospital_id': listing.hospital_id,
        }

    listing = get_listing(id)
    score = 0
    if listing.organ == Listing.Organ.LIVER:
        organ = db.session.query(Liver).filter_by(listing_id=id).first()
        if organ is None:
            raise NotFoundError("L'organe n'a pas été trouvé")
        score = organ.score
    if listing.organ == Listing.Organ.LUNG:
        return compute_matches(id)

    return sorted(
        [
            {
                "listing": schemaify(listing),
                "score": score,
            }
            for listing in db.session.query(Listing).filter_by(
                organ=listing.organ
            )
        ],
        key=lambda x: x['score'],
        reverse=True,
    )
