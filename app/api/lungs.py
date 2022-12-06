from pydantic import BaseModel

from app import db
from app.api.person import get_person
from app.db.models import Listing, Lung
from app.errors import NotFoundError
from app.score.lungs.LungsScore import lungs_final_score
from app.utils.bp import Blueprint

bp = Blueprint(__name__)

class LungSchema(BaseModel):
    diagnosis_group: str
    detailed_diagnosis: Lung.DetailedDiagnosis | None
    body_mass_index: float
    diabetes: bool
    assistance_required: bool
    FVC_percentage: float
    PA_systolic: float
    oxygen_requirement: float
    six_minutes_walk_distance_over_150_feet: bool
    continuous_mech_ventilation: bool
    PCO2: float
    PCO2_increase_superior_to_15_percent: bool

    age_at_transplant: int
    creatinine_at_transplant: float
    ADL_required: bool
    PCW_over_20_mmHg: bool


@bp.get('/<int:listing_id>', success=201)
def get_lungs(listing_id: int):
    lung = db.session.query(Lung).filter_by(listing_id=listing_id).first()
    if not lung:
        raise NotFoundError('No Listing found')
    return lung

def compute_matches(listing_id: int):
    listing_lungs_receivers = (
        db.session.query(Listing)
        .filter(
            Listing.id != listing_id,
            Listing.type == "RECEIVER",
            Listing.organ == "LUNG",
        )
        .all()
    )
    result_listing = []
    for listing_lungs_receiver in listing_lungs_receivers:
        person_receiver = get_person(listing_lungs_receiver.person_id)
        result_listing.append([listing_lungs_receiver, lungs_final_score(person_receiver, None, listing_lungs_receiver)])
    return result_listing