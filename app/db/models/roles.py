import sqlalchemy as sa
from sqlalchemy import event, orm

from app import db


class Role(db.Base):
    can_edit_users = sa.Column(sa.Boolean, default=False)
    can_edit_hospitals = sa.Column(sa.Boolean, default=False)
    can_edit_listings = sa.Column(sa.Boolean, default=False)
    can_edit_staff = sa.Column(sa.Boolean, default=False)
    can_edit_roles = sa.Column(sa.Boolean, default=False)
    can_edit_persons = sa.Column(sa.Boolean, default=False)
    name = sa.Column(sa.String, nullable=False, unique=True)

    users = orm.relationship('User', back_populates='role')

    @classmethod
    def init_table(cls):
        admin = cls(
            can_edit_users=True,
            can_edit_hospitals=True,
            can_edit_listings=True,
            can_edit_staff=True,
            can_edit_roles=True,
            can_edit_persons=True,
            name='admin',
        )
        default = cls(
            can_edit_users=False,
            can_edit_hospitals=False,
            can_edit_listings=False,
            can_edit_staff=False,
            can_edit_roles=False,
            can_edit_persons=False,
            name='default',
        )
        db.session.add_all([admin, default])
        db.session.commit()

    @classmethod
    @property
    def default(cls):
        return db.session.query(cls).filter_by(name='default').first()

    @classmethod
    @property
    def admin(cls):
        return db.session.query(cls).filter_by(name='admin').first()


@event.listens_for(Role.__table__, "after_create")
def roles_table_created(*args, **kwargs):
    Role.init_table()
