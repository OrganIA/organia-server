from app import db
from app.db.models import Role, User

from . import fake


def main():
    mail_provider = "organia.fr"

    db.session.add_all(
        [
            User(
                email=f"admin@{mail_provider}",
                firstname="Jean",
                lastname="Bon",
                phone_number=fake.phone_number(),
                password="admin",
                role=Role.admin,
            ),
            User(
                email=f"admin2@{mail_provider}",
                firstname="Patrick",
                lastname="Dupont",
                phone_number=fake.phone_number(),
                password="admin",
                role=Role.admin,
            ),
            *[
                User(
                    email=f"user{i}@{mail_provider}",
                    firstname=fake.first_name(),
                    lastname=fake.last_name(),
                    phone_number=fake.phone_number(),
                )
                for i in range(10)
            ],
        ]
    )
