import enum

import sqlalchemy as sa

from app import db
from app.db.mixins import OrganMixin
from app.utils.enums import EnumStr


class Lung(OrganMixin, db.Base):
    class DetailedDiagnosis(EnumStr):
        Bronchiectasis = enum.auto()
        Eisenmenger = enum.auto()
        Bronchiolitis = enum.auto()
        Lymphangioleiomyomatosis = enum.auto()
        Sarcoidosis = enum.auto()

    class DiagnosisGroup(EnumStr):
        A = enum.auto()
        B = enum.auto()
        C = enum.auto()
        D = enum.auto()

    diagnosis_group = sa.Column(sa.Enum(DiagnosisGroup))
    detailed_diagnosis = sa.Column(sa.Enum(DetailedDiagnosis))

    body_mass_index = sa.Column(sa.Float)
    diabetes = sa.Column(sa.Boolean)
    assistance_required = sa.Column(sa.Boolean)
    FVC_percentage = sa.Column(sa.Float)
    PA_systolic = sa.Column(sa.Float)
    oxygen_requirement = sa.Column(sa.Float)
    six_minutes_walk_distance_over_150_feet = sa.Column(sa.Boolean)
    continuous_mech_ventilation = sa.Column(sa.Boolean)
    PCO2 = sa.Column(sa.Float)
    PCO2_increase_superior_to_15_percent = sa.Column(sa.Boolean)

    age_at_transplant = sa.Column(sa.Integer)
    creatinine_at_transplant = sa.Column(sa.Float)
    ADL_required = sa.Column(sa.Boolean)
    PCW_over_20_mmHg = sa.Column(sa.Boolean)
