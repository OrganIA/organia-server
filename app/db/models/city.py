import sqlalchemy as sa

from app import db


class City(db.Base):
    name = sa.Column(sa.String)
    department_code = sa.Column(sa.String)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department_code': self.department_code,
        }
