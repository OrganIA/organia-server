import enum

import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.helpers.enums import EnumStr


class Heart(db.Base):
    class URGENCE(EnumStr):
        XPCA = enum.auto()
        XPCP1 = enum.auto()
        XPCP2 = enum.auto()
        NA = enum.auto()

    listing_id = sa.Column(sa.ForeignKey('listings.id'))
    taille_D = sa.Column(sa.Float)
    poids_D = sa.Column(sa.Float)
    ABO_D = sa.Column(sa.String)
    sex_D = sa.Column(sa.String)
    R_D_NAI = sa.Column(sa.Date)
    D_INSC = sa.Column(sa.Date)
    MAL = sa.Column(
        sa.String
    )  # ['Maladie valvulaire', 'Maladie congenitale', 'Maladie congenitale non Eisenmenger',]
    MAL2 = sa.Column(sa.String)
    MAL3 = sa.Column(sa.String)
    urgence = sa.Column(sa.Enum(URGENCE))
    KXPC = sa.Column(sa.String)
    XPC = sa.Column(sa.Integer)
    DRG = sa.Column(sa.String)
    CEC = sa.Column(sa.String)
    SIAV = sa.Column(sa.String)
    CAT = sa.Column(sa.String)
    BNP = sa.Column(sa.Integer)
    DBNP = sa.Column(sa.Integer)
    PROBNP = sa.Column(sa.Float)
    DPROBNP = sa.Column(sa.Date)
    DIA = sa.Column(sa.String)
    CREAT = sa.Column(sa.Float)
    DCREAT = sa.Column(sa.Date)
    BILI = sa.Column(sa.Float)
    DBILI = sa.Column(sa.Date)
    BNP_AVI = sa.Column(sa.Float)
    PBN_AVI = sa.Column(sa.Float)
    DIA_AVI = sa.Column(sa.String)
    CRE_AVI = sa.Column(sa.Float)
    BILI_AVI = sa.Column(sa.Float)
    TTLGP = sa.Column(sa.Float)
    ICAR = sa.Column(sa.Float)
    F_ICAR = sa.Column(sa.Float)
    delai_var_bio_GRF = sa.Column(sa.Date)
    date_courante = sa.Column(sa.Date)

    listing = orm.relationship('Listing', back_populates='heart')
