import sqlalchemy as sa

from app import db


class Lung(db.Base):
    listing_id = sa.Column(sa.ForeignKey('listings.id'))

    diagnosis_group = sa.Column(sa.String, nullable=True, default="")
    detailled_diagnosis = sa.Column(sa.String, nullable=True,default="")

    body_mass_index = sa.Column(sa.Float, nullable=True, default=0)
    diabetes = sa.Column(sa.Boolean, nullable=True, default=False)
    assistance_required = sa.Column(sa.Boolean, nullable=True, default=False)
    FVC_percentage = sa.Column(sa.Float, nullable=True, default=0)
    PA_systolic = sa.Column(sa.Float, nullable=True, default=0)
    oxygen_requirement = sa.Column(sa.Float, nullable=True, default=0)
    six_minutes_walk_distance_over_150_feet = sa.Column(sa.Boolean, nullable=True, default=False)
    continuous_mech_ventilation = sa.Column(sa.Boolean, nullable=True, default=False)
    PCO2 = sa.Column(sa.Float, nullable=True, default=0)
    PCO2_increase_superior_to_15_percent = sa.Column(sa.Boolean, nullable=True, default=False)

    age_at_transplant = sa.Column(sa.Integer, nullable=True, default=0)
    creatinine_at_transplant = sa.Column(sa.Float, nullable=True, default=0)
    ADL_required = sa.Column(sa.Boolean, nullable=True, default=False)
    PCW_over_20_mmHg = sa.Column(sa.Boolean, nullable=True, default=False)

    score = sa.Column(sa.Float, nullable=True, default=0)