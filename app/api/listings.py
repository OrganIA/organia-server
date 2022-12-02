from app import db
from app.db.models import Listing
from app.errors import NotFoundError
from app.utils.bp import Blueprint

bp = Blueprint('listings')


@bp.get('/')
def get_listings():
    return db.session.query(Listing)


@bp.get('/<int:id>')
def get_listing(id):
    result = db.session.get(Listing, id)
    if not result:
        raise NotFoundError
    return result


@bp.get('/<int:id>/matches')
def get_listing_matches(id):
    # TODO
    import random

    def schemaify(listing: Listing):
        return {
            'id': listing.id,
            'type': listing.type,
            'notes': listing.notes,
            'organ': listing.organ,
            'person_id': listing.person_id,
            'hospital_id': listing.hospital_id,
        }

    return sorted(
        [
            {
                "listing": schemaify(listing),
                "score": random.random(),
            }
            for listing in db.session.query(Listing)
        ],
        key=lambda x: x['score'],
        reverse=True,
    )
