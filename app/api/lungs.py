import logging

from pydantic import BaseModel

from app import db
from app.api.person import get_person
from app.db.models import Listing, Lung
from app.errors import NotFoundError
from app.score.lungs.LungsScore import lungs_final_score
from app.utils.bp import Blueprint

bp = Blueprint(__name__)

class LungSchema(BaseModel):
    diagnosis_group: str | None
    detailed_diagnosis: str | None
    body_mass_index: float | None
    diabetes: bool | None
    assistance_required: bool | None
    FVC_percentage: float | None
    PA_systolic: float | None
    oxygen_requirement: float | None
    six_minutes_walk_distance_over_150_feet: bool | None
    continuous_mech_ventilation: bool | None
    PCO2: float | None
    PCO2_increase_superior_to_15_percent: bool | None

    age_at_transplant: int | None
    creatinine_at_transplant: float | None
    ADL_required: bool | None
    PCW_over_20_mmHg: bool | None


@bp.get('/<int:listing_id>', success=201)
def get_lungs(listing_id: int):
    lung = db.session.query(Lung).filter_by(listing_id=listing_id).first()
    if not lung:
        raise NotFoundError('No Listing found')
    return lung


@bp.get('/<int:listing_id>/score_del', success=201)
def delete_lungs_score(listing_id: int):
    listing = db.session.query(Listing).filter_by(id=listing_id).first()
    if listing is None:
        raise NotFoundError(
            'listing_id', listing_id, 'doesn\'t refer to an existing listing'
        )
    lung = get_lungs(listing_id)
    lung.score = 0.0
    db.session.commit()
    return


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