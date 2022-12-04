from datetime import datetime

from app import db
from app.api.person import get_person
from app.db.models import Kidney, Listing
from app.errors import InvalidRequest, NotFoundError
from app.score.kidney.kidney_score import get_score_NAP
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint(__name__)

class KidneyCreateSchema(Static):
    listing_id = int
    
    isDialyse = bool
    isRetransplantation = bool
    def startDateDialyse(self):
        startDateDialyse = Static._get(self, 'startDateDialyse')
        return datetime.fromisoformat(startDateDialyse).date()
    def ARFDate(self):
        ARFDate = Static._get(self, 'ARFDate')
        return datetime.fromisoformat(ARFDate).date()
    def DateTransplantation(self):
        DateTransplantation = Static._get(self, 'DateTransplantation')
        return datetime.fromisoformat(DateTransplantation).date()
    def ReRegistrationDate(self):
        ReRegistrationDate = Static._get(self, 'ReRegistrationDate')
        return datetime.fromisoformat(ReRegistrationDate).date()

class KidneyUpdateScoreSchema(Static):
    score = int


@bp.get('/', success=201)
def get_kidneys():
    return db.session.query(Kidney)


@bp.get('/<int:listing_id>', success=201)
def get_kidney(listing_id):
    result = db.session.query(Kidney).filter_by(listing_id=listing_id).first()
    if not result:
        raise NotFoundError
    return result


@bp.post('/<int:listing_id>', success=201)
def create_kidney_entry(listing_id, data: KidneyCreateSchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    listing_kidney = db.session.query(Kidney).filter_by(
        listing_id=listing_id).first()
    if listing_kidney != None:
        raise InvalidRequest('A listing with this id already exists')

    data.listing_id = listing_id
    data = data.dict(exclude_unset=True)
    kidney = db.add(Kidney, data)
    return kidney


async def update_kidney_score(listing_id: int, data: KidneyUpdateScoreSchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    kidney = await get_kidneys(listing_id)
    kidney.score = data.score
    db.session.commit()
    return kidney


@bp.get('/<int:listing_id>/score_del', success=201)
async def delete_kidney_score(listing_id: int):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('listing_id', listing_id,
                            'doesn\'t refer to an existing listing')
    kidney = await get_kidneys(listing_id)
    kidney.score = 0.0
    db.session.commit()
    return kidney


@bp.get('/<int:listing_id>/matches', status_code=201) #UNCOMMENT WHEN PERSONS IMPLEMENTED
async def compute_matches(listing_id: int):
    donor_listing = db.session.query(
        Listing).filter(listing_id == Listing.id).first()
    if donor_listing == None:
        raise NotFoundError(
            'Id provided doest not refer to an existing listing')
    if donor_listing.donor == False:
        raise InvalidRequest('This listing is a receiver not a donor')
    receivers_listings = db.session.query(Listing).filter(
        Listing.id != listing_id, Listing.donor == False, Listing.organ == "KIDNEY").all()
    donor_person = await get_person(listing_id)
    listings_ids = []
    for receiver in receivers_listings:
        hasKidneyData = db.session.query(Kidney).filter(
            Kidney.listing_id == receiver.id).all()
        if hasKidneyData == []:
            continue
        listings_ids.append(receiver.id)
        receiver_listing_person = await get_person(receiver.person_id)
        score = get_score_NAP(receiver_listing_person, donor_person, receiver)
        await update_kidney_score(receiver.id, score)
    return db.session.query(Kidney).filter(Kidney.listing_id.in_(listings_ids)).order_by(Kidney.score.desc()).all()