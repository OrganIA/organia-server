listing = {
    "hospital_id": 1,
    "notes": "Ce test est un test",
    "person_id": 1,
    "type": "DONOR",
    "organ_type": "LIVER",
    "start_date": "2022-12-05",
    "end_date": "2022-12-05",
    "weight_kg": 81.0,
    "height_cm": 187.2,
}

update_listing = {
    "hospital_id": 1,
    "notes": "Ce test est une update",
    "person_id": 1,
    "type": "RECEIVER",
    "organ_type": "KIDNEY",
    "start_date": "2022-12-05",
    "end_date": "2022-12-05",
    "weight_kg": 71.0,
    "height_cm": 167.2,
}


def test_get_listing(client):
    response = client.post('/api/listings/', json=listing)
    assert response.status_code == 200
    response = client.get('/api/listings/1')
    assert response.status_code == 200


def test_get_listings(client):
    response = client.get('/api/listings/', json=listing)
    assert response.status_code == 200


def test_create_listing(client):
    response = client.post('/api/listings/', json=listing)
    assert response.status_code == 200


def test_update_listing(client):
    response = client.post('/api/listings/', json=listing)
    assert response.status_code == 200
    response = client.post('/api/listings/1', json=update_listing)
    assert response.status_code == 200


def test_delete_listing(client):
    response = client.post('/api/listings/', json=listing)
    assert response.status_code == 200
    response = client.delete('/api/listings/1', json=update_listing)
    assert response.status_code == 204
