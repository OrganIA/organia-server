import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.db.mixins import TimedMixin


class Liver(TimedMixin, db.Base):
    listing_id = sa.Column(sa.ForeignKey('listings.id'))
    tumors_number = sa.Column(sa.Integer, default=0)
    biggest_tumor_size = sa.Column(sa.Integer)
    alpha_fetoprotein = sa.Column(sa.Integer)
    listing = orm.relationship('Listing', back_populates='liver')

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
