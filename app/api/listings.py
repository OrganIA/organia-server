from app import db
from app.db.models import Listing
from app.errors import NotFoundError
from app.utils.bp import Blueprint
from app.utils.static import Static

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

    return [
        {
            "listing": "data",
            "score": random.random(),
        }
        for _ in range(10)
    ]
