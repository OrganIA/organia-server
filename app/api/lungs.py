from app import db
from app.db.models import Listing, Lung
from app.errors import InvalidRequest, NotFoundError
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint(__name__)


class LungCreateSchema(Static):
    listing_id = int

    diagnosis_group = str
    detailed_diagnosis = str
    body_mass_index = float
    diabetes = bool
    assistance_required = bool
    FVC_percentage = float
    PA_systolic = float
    oxygen_requirement = float
    six_minutes_walk_distance_over_150_feet = bool
    continuous_mech_ventilation = bool
    PCO2 = float
    PCO2_increase_superior_to_15_percent = bool

    age_at_transplant = int
    creatinine_at_transplant = float
    ADL_required = bool
    PCW_over_20_mmHg = bool

class LungUpdateScoreSchema(Static):
    score = int


@bp.get('/<int:listing_id', success=201)
async def get_lungs(listing_id: int):
    query = db.session.query(Lung).filter_by(listing_id=listing_id).first()
    if not query:
        raise NotFoundError('No Listing found')
    return query


@bp.post('/<int:listing_id>', success=201)
async def update_lungs_variables(listing_id: int, data: LungCreateSchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    listing_lung = db.session.query(Lung).filter_by(
        listing_id=listing_id).first()
    if listing_lung != None:
        raise InvalidRequest('A listing with this id already exists')

    data.listing_id = listing_id
    data = data.dict(exclude_unset=True)
    lungs = db.add(Lung, data)
    return lungs


@bp.post('/<int:listing_id>/score', success=201)
async def update_lungs_score(listing_id: int, score: LungUpdateScoreSchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    lung = await get_lungs(listing_id)
    lung.score = score.score
    db.session.commit()
    return lung


@bp.get('/<int:listing_id>/score_del', success=201)
async def delete_lungs_score(listing_id: int):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('listing_id', listing_id,
                            'doesn\'t refer to an existing listing')
    lung = await get_lungs(listing_id)
    lung.score = 0.0
    db.session.commit()
    return