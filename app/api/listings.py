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
