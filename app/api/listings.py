import importlib
from datetime import date

import flask
from pydantic import BaseModel

from app import db
from app.api.person import PersonCreateSchema, PersonSchema
from app.db.models import Listing, Person
from app.errors import InvalidRequest, NotFoundError
from app.utils.bp import Blueprint

bp = Blueprint(__name__)


class ListingSchema(BaseModel):
    hospital_id: int | None
    notes: str | None
    person_id: int | None
    person: PersonSchema | None
    type: Listing.Type | None
    organ_type: Listing.Organ | None
    organ: dict | None
    person: PersonSchema | None
    start_date: date | None
    end_date: date | None
    weight_kg: float | None
    height_cm: float | None


class ListingCreateSchema(ListingSchema):
    person: PersonCreateSchema | None


def get_organ_data(organ_type, data, update=False) -> dict:
    schemas_module = importlib.import_module('app.api.organs')
    schema_name = organ_type.value.capitalize()
    if update:
        schema_name += 'Update'
    schema_name += 'Schema'
    schema: BaseModel = getattr(schemas_module, schema_name)
    return schema(**data).dict(exclude_unset=True)


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
def create_listing(data: ListingCreateSchema):
    data = data.dict()
    organ_data = data.pop("organ", None)
    organ_type = data.get("organ_type", None)
    if organ_type and organ_data:
        organ_data = get_organ_data(organ_type, organ_data)
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
    data = data.dict(exclude_unset=True)
    organ_data = data.pop("organ", None)
    if organ_data:
        organ_type = data.get("organ_type", listing.organ_type)
        organ_data = get_organ_data(organ_type, organ_data, update=True)
        if listing.organ:
            listing.organ.read_dict(organ_data)
        else:
            organ_type.table(**organ_data, listing=listing)
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
    receivers = filter(lambda x: x.organ, receivers)
    organ_name = listing.organ_type.value.lower()
    score_module = importlib.import_module(
        f'app.score.{organ_name}.{organ_name}_score'
    )
    score_func = getattr(score_module, f'compute_{organ_name}_score')
    return {
        "donor": listing,
        "matches": sorted(
            [
                {"receiver": receiver, "score": score_func(listing, receiver)}
                for receiver in receivers
            ],
            key=lambda x: x['score'],
            reverse=True,
        ),
    }
