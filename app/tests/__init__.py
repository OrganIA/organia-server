from fastapi.testclient import TestClient

from app.main import app
from app.api import PREFIX


client = TestClient(app)
