import enum

import sqlalchemy as sa

from app import db
from app.db.mixins import OrganMixin
from app.helpers.enums import EnumStr


class Heart(OrganMixin, db.Base):
    class Emergency(EnumStr):
        XPCA = enum.auto()
        XPCP1 = enum.auto()
        XPCP2 = enum.auto()
        NA = enum.auto()

    class DiagnosisGroup(EnumStr):
        VALVULAR = enum.auto()
        CONGENITAL = enum.auto()
        CONGENITAL_NON_EISENMENGER = enum.auto()

    delay_var_bio_GRF = sa.Column(sa.Integer)
    emergency = sa.Column(sa.Enum(Emergency))
    weight_kg = sa.Column(sa.Float)
    height_cm = sa.Column(sa.Float)

    MAL = sa.Column(sa.Enum(DiagnosisGroup))
    MAL2 = sa.Column(sa.Enum(DiagnosisGroup))
    MAL3 = sa.Column(sa.Enum(DiagnosisGroup))

    DA = sa.Column(sa.Integer)
    DAURG = sa.Column(sa.Integer)
    XPC = sa.Column(sa.Integer)

    BILI = sa.Column(sa.Float)
    CREAT = sa.Column(sa.Float)
    F_ICAR = sa.Column(sa.Float)
    ICAR = sa.Column(sa.Float)
    KXPC = sa.Column(sa.Float)

    DIA_is_O = sa.Column(sa.Boolean)

    DBILI = sa.Column(sa.Date)
    DCREAT = sa.Column(sa.Date)
