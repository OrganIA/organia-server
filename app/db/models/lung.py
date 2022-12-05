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

    body_mass_index = sa.Column(sa.Float, default=0)
    diabetes = sa.Column(sa.Boolean, default=False)
    assistance_required = sa.Column(sa.Boolean, default=False)
    FVC_percentage = sa.Column(sa.Float, default=0)
    PA_systolic = sa.Column(sa.Float, default=0)
    oxygen_requirement = sa.Column(sa.Float, default=0)
    six_minutes_walk_distance_over_150_feet = sa.Column(
        sa.Boolean, default=False
    )
    continuous_mech_ventilation = sa.Column(sa.Boolean, default=False)
    PCO2 = sa.Column(sa.Float, default=0)
    PCO2_increase_superior_to_15_percent = sa.Column(sa.Boolean, default=False)

    age_at_transplant = sa.Column(sa.Integer, default=0)
    creatinine_at_transplant = sa.Column(sa.Float, default=0)
    ADL_required = sa.Column(sa.Boolean, default=False)
    PCW_over_20_mmHg = sa.Column(sa.Boolean, default=False)

    listing = orm.relationship('Listing', backref="listings", uselist=False)

    score = sa.Column(sa.Float, default=0)
