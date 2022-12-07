import enum
from cmath import isnan
from datetime import datetime
from math import ceil as round

import numpy as np
import sqlalchemy as sa
from numpy import log as ln
from sqlalchemy import orm

from app import db
from app.db.mixins import TimedMixin
from app.helpers.enums import EnumStr


class Heart(TimedMixin, db.Base):
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
    MAL = sa.Column(sa.String)
    MAL2 = sa.Column(sa.String)
    MAL3 = sa.Column(sa.String)
    urgence = sa.Column(sa.Enum(URGENCE))
    d_urgence = sa.Column(sa.Date)
    KXPC = sa.Column(sa.String)
    XPC = sa.Column(sa.Integer)
    DRG = sa.Column(sa.String)
    CEC = sa.Column(sa.String)
    DCEC = sa.Column(sa.Date)
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
    comp_ad_std = sa.Column(sa.Float)
    comp_ad_XPCA = sa.Column(sa.Float)
    comp_ped_std = sa.Column(sa.Float)
    comp_ped_XPCP = sa.Column(sa.Float)
    score_CCB = sa.Column(sa.Float)
    F1_dif_age = sa.Column(sa.Boolean)
    F2_ABO = sa.Column(sa.Boolean)
    F3_SC = sa.Column(sa.Boolean)
    F4_surv_post_GRF = sa.Column(sa.Boolean)
    score_CCP = sa.Column(sa.Float)
    score_NACG = sa.Column(sa.Float)
    D_D_NAI = sa.Column(sa.Date)
    D_PREL = sa.Column(sa.Date)
    score = sa.Column(sa.Float, default=0)

    listing = orm.relationship('Listing', back_populates='heart')
