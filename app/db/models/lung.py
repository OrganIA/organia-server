import sqlalchemy as sa

from app import db


class Lung(db.Base):
    listing_id = sa.Column(sa.ForeignKey('listings.id'))

    diagnosis_group = sa.Column(sa.String, nullable=True)
    detailed_diagnosis = sa.Column(sa.String, nullable=True)

    body_mass_index = sa.Column(sa.Float, nullable=True)
    diabetes = sa.Column(sa.Boolean, nullable=True)
    assistance_required = sa.Column(sa.Boolean, nullable=True)
    FVC_percentage = sa.Column(sa.Float, nullable=True)
    PA_systolic = sa.Column(sa.Float, nullable=True)
    oxygen_requirement = sa.Column(sa.Float, nullable=True)
    six_minutes_walk_distance_over_150_feet = sa.Column(sa.Boolean, nullable=True)
    continuous_mech_ventilation = sa.Column(sa.Boolean, nullable=True)
    PCO2 = sa.Column(sa.Float, nullable=True)
    PCO2_increase_superior_to_15_percent = sa.Column(sa.Boolean, nullable=True)

    age_at_transplant = sa.Column(sa.Integer, nullable=True)
    creatinine_at_transplant = sa.Column(sa.Float, nullable=True)
    ADL_required = sa.Column(sa.Boolean, nullable=True)
    PCW_over_20_mmHg = sa.Column(sa.Boolean, nullable=True)

    score = sa.Column(sa.Float, nullable=True, default=0)