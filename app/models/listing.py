import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.helpers.enums import EnumStr


class Listing(db.DurationMixin, db.Base):
    class Organ(EnumStr):
        HEART = enum.auto()
        KIDNEY = enum.auto()
        LIVER = enum.auto()
        LUNG = enum.auto()

    person_id = sa.Column(sa.ForeignKey('persons.id'))
    notes = sa.Column(sa.String)
    hospital_id = sa.Column(sa.ForeignKey('hospitals.id'))
    donor = sa.Column(sa.Boolean, default=False, nullable=False)
    tumors_number = sa.Column(sa.Integer, default=0, nullable=False)
    biggest_tumor_size = sa.Column(sa.Integer, nullable=True)
    alpha_fetoprotein = sa.Column(sa.Integer, nullable=True)
    organ = sa.Column(sa.Enum(Organ))
    isDialyse = sa.Column(sa.Boolean, default=False, nullable=True)
    isRetransplantation = sa.Column(sa.Boolean, default=False, nullable=True)
    startDateDialyse = sa.Column(sa.Date, nullable=True)
    EndDateDialyse = sa.Column(sa.Date, nullable=True)
    ARFDate = sa.Column(sa.Date, nullable=True)
    DateTransplantation = sa.Column(sa.Date, nullable=True)
    ReRegistrationDate = sa.Column(sa.Date, nullable=True)
    A = sa.Column(sa.Integer, default=0, nullable=True)
    B = sa.Column(sa.Integer, default=0, nullable=True)
    DR = sa.Column(sa.Integer, default=0, nullable=True)
    DQ = sa.Column(sa.Integer, default=0, nullable=True)

    body_mass_index = sa.Column(sa.Float, default=0, nullable=True)
    diabetes = sa.Column(sa.Boolean, default=False, nullable=True)
    functional_status_assistance_required = sa.Column(
        sa.Boolean, default=False, nullable=True)
    FVC_percentage = sa.Column(sa.Float, default=0, nullable=True)
    PA_systolic = sa.Column(sa.Float, default=0, nullable=True)
    oxygen_requirement = sa.Column(sa.Float, default=0, nullable=True)
    six_minute_walk_distance_over_150_feet = sa.Column(
        sa.Boolean, default=True, nullable=True)
    continuous_mechanical_ventilation = sa.Column(
        sa.Boolean, default=False, nullable=True)
    PC02 = sa.Column(sa.Float, default=40, nullable=True)
    PCO2_increase_superior_to_15_percent = sa.Column(
        sa.Boolean, default=False, nullable=True)
    diagnosis_group = sa.Column(sa.String, default="A", nullable=True)
    detailled_diagnosis = sa.Column(sa.String, nullable=True)

    person = orm.relationship('Person', backref='listings')
    hospital = orm.relationship('Hospital', backref='listings')

    @property
    def alpha_fetoprotein_score(self):
        if (self.tumors_number == 0
            or self.biggest_tumor_size is None
                or self.alpha_fetoprotein is None):
            return 0
        alpha_fetoprotein_score = 0
        if (self.tumors_number >= 4):
            alpha_fetoprotein_score += 2
        if (self.biggest_tumor_size > 3 and self.biggest_tumor_size <= 6):
            alpha_fetoprotein_score += 1
        elif (self.biggest_tumor_size > 6):
            alpha_fetoprotein_score += 4
        if (self.alpha_fetoprotein > 100 and self.alpha_fetoprotein <= 1000):
            alpha_fetoprotein_score += 2
        elif (self.alpha_fetoprotein > 1000):
            alpha_fetoprotein_score += 3
        return alpha_fetoprotein_score
