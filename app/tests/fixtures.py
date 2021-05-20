import os
import pytest
from app import db


@pytest.fixture(autouse=True)
def clean_db():
    db.setup_db(url=os.environ.get('DB_URL', 'sqlite:///'), force=True)
    db.Base.metadata.create_all(bind=db.engine)
