def test_should_status_code_ok(client):
    response = client.get('/api/')
    assert response.status_code == 200


def test_get_listing(client):
    response = client.get('/api/listings/')
    assert response.status_code == 200
