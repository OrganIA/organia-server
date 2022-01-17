import os
import pytest

from app import db
from . import client


def create_admin():
    from app.models import LoginToken, User
    user = User(email='admin', role=1)
    db.session.add(user)
    db.session.commit()
    token = LoginToken.get_valid_for_user(user)
    db.session.commit()
    return token.value


@pytest.fixture(autouse=True)
def clean_db():
    db.setup_db(url=os.environ.get('DB_URL', 'sqlite:///'), force=True)
    db.Base.metadata.create_all(bind=db.engine)
    client.headers['authorization'] = f'Bearer {create_admin()}'
