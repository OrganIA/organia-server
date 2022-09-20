import sqlalchemy as sa
from sqlalchemy.sql.expression import null

from app import db

class Liver(db.TimedMixin, db.Base):
    listing_id = sa.Column(sa.ForeignKey('listings.id'))
    tumors_number = sa.Column(sa.Integer, default=0, nullable=True)
    biggest_tumor_size = sa.Column(sa.Integer, nullable=True)
    alpha_fetoprotein = sa.Column(sa.Integer, nullable=True)
    score = sa.Column(sa.Float, nullable=True, default=0)

    @property
    def alpha_fetoprotein_score(self):
        if (self.tumors_number == 0 \
        or self.biggest_tumor_size is None \
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