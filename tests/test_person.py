person = {
    "first_name": "Nicolas",
    "last_name": "Yapobi",
    "birth_date": "1999-05-18",
    "description": "Digital",
    "abo": "A",
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


def test_failed_create_person(client):
    response = client.post('/api/person/', json=fail_person)
    assert response.status_code == 422
