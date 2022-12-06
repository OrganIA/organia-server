import enum

import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.utils.enums import EnumStr


class Lung(db.Base):
    class DetailedDiagnosis(EnumStr):
        Bronchiectasis = enum.auto()
        Eisenmenger = enum.auto()
        Bronchiolitis = enum.auto()
        Lymphangioleiomyomatosis = enum.auto()
        Sarcoidosis = enum.auto()

    listing_id = sa.Column(sa.ForeignKey('listings.id'))

    diagnosis_group = sa.Column(sa.String, default="")
    detailed_diagnosis = sa.Column(
        sa.Enum(DetailedDiagnosis), default="Bronchiectasis"
    )

    body_mass_index = sa.Column(sa.Float)
    diabetes = sa.Column(sa.Boolean)
    assistance_required = sa.Column(sa.Boolean)
    FVC_percentage = sa.Column(sa.Float)
    PA_systolic = sa.Column(sa.Float)
    oxygen_requirement = sa.Column(sa.Float)
    six_minutes_walk_distance_over_150_feet = sa.Column(
        sa.Boolean
    )
    continuous_mech_ventilation = sa.Column(sa.Boolean)
    PCO2 = sa.Column(sa.Float)
    PCO2_increase_superior_to_15_percent = sa.Column(sa.Boolean)

    age_at_transplant = sa.Column(sa.Integer)
    creatinine_at_transplant = sa.Column(sa.Float)
    ADL_required = sa.Column(sa.Boolean)
    PCW_over_20_mmHg = sa.Column(sa.Boolean)

    listing = orm.relationship('Listing', back_populates="lung", uselist=False)