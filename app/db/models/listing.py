import enum

import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.utils.enums import EnumStr


class Listing(db.Base):
    class Type(EnumStr):
        DONOR = enum.auto()
        PATIENT = enum.auto()

    class Organ(EnumStr):
        HEART = enum.auto()
        KIDNEY = enum.auto()
        LUNG = enum.auto()

    # fields

    notes = sa.Column(sa.String)
    type = sa.Column(sa.Enum(Type))
    organ = sa.Column(sa.Enum(Organ))

    # algo fields

    tumors_number = sa.Column(sa.Integer, default=0, nullable=False)
    biggest_tumor_size = sa.Column(sa.Integer, nullable=True)
    alpha_fetoprotein = sa.Column(sa.Integer, nullable=True)
    # specific to kidneys?
    is_under_dialysis = sa.Column(sa.Boolean, default=False, nullable=True)
    # can only have one dialysis report?
    dialysis_start_date = sa.Column(sa.Date, nullable=True)
    dialysis_end_date = sa.Column(sa.Date, nullable=True)
    is_retransplantation = sa.Column(sa.Boolean, default=False, nullable=True)
    # what does ARF mean?
    arf_date = sa.Column(sa.Date, nullable=True)
    # isn't this the same as end_date?
    transplantation_date = sa.Column(sa.Date, nullable=True)
    # isbn't this just having 2 listings?
    re_registration_date = sa.Column(sa.Date, nullable=True)
    # no idea what this is, should be more specific
    A = sa.Column(sa.Integer, default=0, nullable=True)
    B = sa.Column(sa.Integer, default=0, nullable=True)
    DR = sa.Column(sa.Integer, default=0, nullable=True)
    DQ = sa.Column(sa.Integer, default=0, nullable=True)

    # relationships

    person_id = sa.Column(sa.ForeignKey('persons.id'))
    hospital_id = sa.Column(sa.ForeignKey('hospitals.id'))

    person = orm.relationship('Person', backref='listings')
    hospital = orm.relationship('Hospital', backref='listings')

    @property
    def alpha_fetoprotein_score(self):
        if (
            self.tumors_number == 0
            or self.biggest_tumor_size is None
            or self.alpha_fetoprotein is None
        ):
            return 0
        alpha_fetoprotein_score = 0
        if self.tumors_number >= 4:
            alpha_fetoprotein_score += 2
        if self.biggest_tumor_size > 3 and self.biggest_tumor_size <= 6:
            alpha_fetoprotein_score += 1
        elif self.biggest_tumor_size > 6:
            alpha_fetoprotein_score += 4
        if self.alpha_fetoprotein > 100 and self.alpha_fetoprotein <= 1000:
            alpha_fetoprotein_score += 2
        elif self.alpha_fetoprotein > 1000:
            alpha_fetoprotein_score += 3
        return alpha_fetoprotein_score