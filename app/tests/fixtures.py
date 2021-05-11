import pytest
from app import db


@pytest.fixture(autouse=True)
def clean_db():
    db.setup_db()
    db.Base.metadata.create_all(bind=db.engine)
