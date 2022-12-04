from app import db
from app.api.person import get_person
from app.db.models import Listing, Lung
from app.errors import NotFoundError
from app.score.lungs.LungsScore import lungs_final_score
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


@bp.get('/<int:listing_id>', success=201)
def get_lungs(listing_id: int):
    query = db.session.query(Lung).filter_by(listing_id=listing_id).first()
    if not query:
        raise NotFoundError('No Listing found')
    return query


def update_lungs_score(listing_id: int, score: LungUpdateScoreSchema):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('Listing not found')
    lung = get_lungs(listing_id)
    lung.score = score
    db.session.commit()
    return lung


@bp.get('/<int:listing_id>/score_del', success=201)
def delete_lungs_score(listing_id: int):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing == None:
        raise NotFoundError('listing_id', listing_id,
                            'doesn\'t refer to an existing listing')
    lung = get_lungs(listing_id)
    lung.score = 0.0
    db.session.commit()
    return

def compute_matches(listing_id: int):
    listing_lungs_receivers = db.session.query(Listing).filter(
        Listing.id != listing_id, Listing.type == "PATIENT", Listing.organ == "LUNG").all()
    listing_lungs_receiver_ids = []
    for listing_lungs_receiver in listing_lungs_receivers:
        listing_lungs_receiver_ids.append(listing_lungs_receiver.id)
        person_receiver =  get_person(listing_lungs_receiver.person_id)
        update_lungs_score(listing_lungs_receiver.id, lungs_final_score(person_receiver, None, listing_lungs_receiver))
    return db.session.query(Lung).filter(Lung.listing_id.in_(listing_lungs_receiver_ids)).order_by(Lung.score.desc()).all()