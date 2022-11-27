from datetime import datetime

from app import db
from app.db.models import Kidney, Listing
from app.errors import InvalidRequest, NotFoundError
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

