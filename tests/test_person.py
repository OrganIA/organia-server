person = {
    "first_name": "Nicolas",
    "last_name": "Yapobi",
    "birth_date": "1999-05-18",
    "description": "Digital",
    "abo": "A",
    "rhesus": "+",
    "gender": "MALE",
}

update_person = {
    "first_name": "Felix",
    "last_name": "Burdot",
    "birth_date": "2000-12-18",
    "description": "IT",
    "abo": "B",
    "rhesus": "+",
    "gender": "MALE",
}

fail_person = {
    "first_name": "Nicolas",
    "last_name": "Yapobi",
    "birth_date": "1999-05-18",
    "description": "Digital",
    "abo": "A",
}


def test_create_person(client):
    response = client.post('/api/person/', json=person)
    assert response.status_code == 200


def test_update_person(client):
    response = client.post('/api/person/', json=person)
    assert response.status_code == 200
    response = client.post('/api/person/1', json=update_person)
    assert response.status_code == 200


def test_failed_create_person(client):
    response = client.post('/api/person/', json=fail_person)
    assert response.status_code == 422


def test_delete_person(client):
    response = client.post('/api/person/', json=person)
    assert response.status_code == 200
    response = client.delete('/api/person/1')
    assert response.status_code == 204
