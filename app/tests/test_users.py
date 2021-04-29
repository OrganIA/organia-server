from fastapi.testclient import TestClient

from app.main import app
from app.api import PREFIX

client = TestClient(app)

def test_users():
    response = client.get(f'{PREFIX}/users')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    if result:
        assert 'name' in result[0]
