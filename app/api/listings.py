import logging

import flask
from pydantic import BaseModel

from app import db
from app.api.person import PersonSchema
from app.db.models import Listing, Person
from app.errors import InvalidRequest, NotFoundError
from app.utils.bp import Blueprint

bp = Blueprint(__name__)


class ListingSchema(BaseModel):
    hospital_id: int | None
    notes: str | None
    person_id: int | None
    type: Listing.Type | None
    organ_type: Listing.Organ | None
    organ: dict | None
    person: PersonSchema | None


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
