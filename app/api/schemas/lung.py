from datetime import date
from optparse import Option
from tokenize import String
from typing import Optional
from app import db
from app.models import lung

class LungSchema(db.Schema):
    listing_id: Optional[int]
    
    diagnosis_group: Optional[str]
    detailed_diagnosis: Optional[str]

    body_mass_index: Optional[float]
    diabetes: Optional[bool]
    assistance_required: Optional[bool]
    FVC_percentage: Optional[float]
    PA_systolic: Optional[float]
    oxygen_requirement: Optional[float]
    six_minutes_walk_distance_over_150_feet: Optional[bool]
    continuous_mech_ventilation: Optional[bool]
    PCO2: Optional[float]
    PCO2_increase_superior_to_15_percent: Optional[bool]

    age_at_transplant: Optional[int]
    creatinine_at_transplant: Optional[float]
    ADL_required: Optional[bool]
    PCW_over_20_mmHg: Optional[bool]
    
    score: Optional[int]

    class Config:
        orm_mode = True


class LungCreateSchema(LungSchema):
    listing_id: Optional[int]
    
    diagnosis_group: Optional[str]
    detailed_diagnosis: Optional[str]

    body_mass_index: Optional[float]
    diabetes: Optional[bool]
    assistance_required: Optional[bool]
    FVC_percentage: Optional[float]
    PA_systolic: Optional[float]
    oxygen_requirement: Optional[float]
    six_minutes_walk_distance_over_150_feet: Optional[bool]
    continuous_mech_ventilation: Optional[bool]
    PCO2: Optional[float]
    PCO2_increase_superior_to_15_percent: Optional[bool]

    age_at_transplant: Optional[int]
    creatinine_at_transplant: Optional[float]
    ADL_required: Optional[bool]
    PCW_over_20_mmHg: Optional[bool]
    
    score: Optional[int]

    class Config:
        orm_mode = True

class LungUpdateSchema(LungSchema):
    diagnosis_group: Optional[str]
    detailed_diagnosis: Optional[str]

    body_mass_index: Optional[float]
    diabetes: Optional[bool]
    assistance_required: Optional[bool]
    FVC_percentage: Optional[float]
    PA_systolic: Optional[float]
    oxygen_requirement: Optional[float]
    six_minutes_walk_distance_over_150_feet: Optional[bool]
    continuous_mech_ventilation: Optional[bool]
    PCO2: Optional[float]
    PCO2_increase_superior_to_15_percent: Optional[bool]

    age_at_transplant: Optional[int]
    creatinine_at_transplant: Optional[float]
    ADL_required: Optional[bool]
    PCW_over_20_mmHg: Optional[bool]

    class Config:
        orm_mode = True