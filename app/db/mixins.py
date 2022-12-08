from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm


@orm.declarative_mixin
class CreatedMixin:
    """Adds a `created_at` column auto-filled with the creation time of the
    row"""

    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)


@orm.declarative_mixin
class TimedMixin(CreatedMixin):
    """Adds a `updated_at` column auto-filled with the last update time of the
    row, in addition to the `created_at` column"""

    updated_at = sa.Column(sa.DateTime, onupdate=datetime.utcnow)


@orm.declarative_mixin
class OrganMixin:
    @orm.declared_attr
    def listing_id(cls):
        return sa.Column(sa.ForeignKey('listings.id'))

    @orm.declared_attr
    def listing(cls):
        return orm.relationship('Listing', uselist=False)
