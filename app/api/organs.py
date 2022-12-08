from datetime import date

from pydantic import BaseModel

from app.db.models import Lung


class KidneySchema(BaseModel):
    is_under_dialysis: bool
    is_retransplantation: bool
    dialysis_start_date: date
    dialysis_end_date: date | None
    arf_date: date
    date_transplantation: date | None
    re_registration_date: date | None
    A: float
    B: float
    DR: float
    DQ: float


class KidneyUpateSchema(KidneySchema):
    is_under_dialysis: bool | None
    is_retransplantation: bool | None
    dialysis_start_date: date | None
    dialysis_end_date: date | None
    arf_date: date | None
    A: float | None
    B: float | None
    DR: float | None
    DQ: float | None


class LiverSchema(BaseModel):
    tumors_count: int
    biggest_tumor_size: int
    alpha_fetoprotein: int


class LiverUpdateSchema(LiverSchema):
    tumors_count: int | None
    biggest_tumor_size: int | None
    alpha_fetoprotein: int | None


class LungSchema(BaseModel):
    diagnosis_group: Lung.DiagnosisGroup
    detailed_diagnosis: Lung.DetailedDiagnosis | None
    body_mass_index: float
    diabetes: bool
    assistance_required: bool
    pulmonary_function_percentage: float
    pulmonary_artery_systolic: float
    oxygen_requirement: float
    six_minutes_walk_distance_over_150_feet: bool
    continuous_mech_ventilation: bool
    carbon_dioxide_partial_pressure: float
    carbon_dioxide_partial_pressure_15_percent_increase: bool
    creatinine: float
    activities_of_daily_life_required: bool
    pulmonary_capilary_wedge_pressure: float


class LungUpdateSchema(LungSchema):
    diagnosis_group: Lung.DiagnosisGroup | None
    body_mass_index: float | None
    diabetes: bool | None
    assistance_required: bool | None
    pulmonary_function_percentage: float | None
    pulmonary_artery_systolic: float | None
    oxygen_requirement: float | None
    six_minutes_walk_distance_over_150_feet: bool | None
    continuous_mech_ventilation: bool | None
    carbon_dioxide_partial_pressure: float | None
    carbon_dioxide_partial_pressure_15_percent_increase: bool | None
    creatinine: float | None
    activities_of_daily_life_required: bool | None
    pulmonary_capilary_wedge_pressure: float | None
