from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

from app.api import PREFIX
from .helpers import assert_response
