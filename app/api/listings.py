import logging

import flask
from pydantic import BaseModel

from app import db
from app.api.kidneys import KidneySchema, compute_matches_kidney
from app.api.livers import LiverSchema
from app.api.lungs import LungSchema, compute_matches_lungs
from app.api.person import PersonSchema
from app.db.models import Kidney, Listing, Liver, Lung, Person
from app.db.models.person import Person
from app.errors import InvalidRequest, NotFoundError
from app.utils.bp import Blueprint

bp = Blueprint(__name__)


class ListingSchema(BaseModel):
    hospital_id: int | None
    notes: str | None
    person_id: int | None
    type: Listing.Type
    liver: LiverSchema | None
    lung: LungSchema | None
    kidney: KidneySchema | None
    person: PersonSchema | None
    type: Listing.Type | None
    organ_type: Listing.Organ | None
    organ: dict | None
    person: PersonSchema | None


def create_organ(data):
    # Update this function when an organ is implemented
    listing = db.session.query(Listing).order_by(Listing.id.desc()).first()
    if not listing:
        raise NotFoundError
    organ = {}
    if listing.organ == Listing.Organ.LIVER:
        organ = Liver()
        organ = update(organ, data)
        organ.listing_id = listing.id
        db.session.add(organ)
        db.session.commit()
    if listing.organ == Listing.Organ.KIDNEY:
        organ = Kidney()
        organ = update(organ, data)
        db.session.add(organ)
        db.session.commit()
    if listing.organ == Listing.Organ.LUNG:
        organ = Lung()
        organ = update(organ, data)
        organ.listing_id = listing.id
        db.session.add(organ)
        db.session.commit()
    return organ


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
    if data.organ == Listing.Organ.KIDNEY:
        organ = db.session.query(Kidney).filter_by(listing_id=id).first()
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
    organ_data = data.pop("organ", None)
    organ_type = data.get("organ_type", None)
    if organ_type and organ_data:
        data['_' + organ_type.value.lower()] = organ_type.table(**organ_data)
    if person_data := data.pop("person", None):
        data['person'] = Person(**person_data)
    listing = Listing(**data)
    db.session.add(listing)
    db.session.commit()
    return listing


@bp.post('/<int:id>')
def update_listing(id, data: ListingSchema):
    listing = get_listing(id)
    data = data.dict()
    listing.read_dict(data)
    db.session.commit()
    return listing


@bp.delete('/<int:id>')
def delete_listing(id: int):
    listing = get_listing(id)
    db.session.delete(listing)
    db.session.commit()


@bp.get('/<int:id>/matches')
def get_listing_matches(id):
    listing = get_listing(id)
    if listing.type != Listing.Type.DONOR:
        raise InvalidRequest("You can only match from a donor")
    receivers = db.session.query(Listing).filter(
        Listing.type == Listing.Type.RECEIVER,
        Listing.organ_type == listing.organ_type,
    )
    return {
        "donor": listing,
        "matches": [
            {
                "receiver": receiver,
                "score": listing.organ.match(receiver),
            }
            for receiver in receivers
        ],
    }
