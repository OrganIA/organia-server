import enum

import sqlalchemy as sa

from app import db
from app.db.mixins import OrganMixin
from app.utils.enums import EnumStr


class Lung(OrganMixin, db.Base):
    class DetailedDiagnosis(EnumStr):
        BRONCHIECTASIS = enum.auto()
        EISENMENGER = enum.auto()
        BRONCHIOLITIS = enum.auto()
        LAM = enum.auto()  # Lymphangioleiomyomatosis
        SARCOIDOSIS = enum.auto()

    class DiagnosisGroup(EnumStr):
        A = enum.auto()
        B = enum.auto()
        C = enum.auto()
        D = enum.auto()

    diagnosis_group = sa.Column(sa.Enum(DiagnosisGroup))
    detailed_diagnosis = sa.Column(sa.Enum(DetailedDiagnosis))

    body_mass_index = sa.Column(sa.Float)  # Tina = 17.9
    diabetes = sa.Column(sa.Boolean)
    assistance_required = sa.Column(sa.Boolean)
    pulmonary_function_percentage = sa.Column(sa.Float)  # FVC, normal = 80%
    pulmonary_artery_systolic = sa.Column(
        sa.Float
    )  # PA systolic, normal = 17 - 20 mmHg, > 30 mmHg = severe
    oxygen_requirement = sa.Column(sa.Float)  # ?
    six_minutes_walk_distance_over_150_feet = sa.Column(
        sa.Boolean
    )  # Test de marche de 6 minutes / 6 MWT > 150 feet
    continuous_mech_ventilation = sa.Column(sa.Boolean)
    carbon_dioxide_partial_pressure = sa.Column(
        sa.Float
    )  # pCO2, normal = 35-40 mmHg
    carbon_dioxide_partial_pressure_15_percent_increase = sa.Column(sa.Boolean)

    # age_at_transplant = sa.Column(sa.Integer)
    creatinine = sa.Column(sa.Float)  # normal = 7-13
    activities_of_daily_life_required = sa.Column(sa.Boolean)
    pulmonary_capilary_wedge_pressure = sa.Column(
        sa.Float
    )  # normal = 4-12 mmHg, > 20 mmHg = severe
