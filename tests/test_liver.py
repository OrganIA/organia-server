person = {
    "first_name": "Nicolas",
    "last_name": "Yapobi",
    "birth_date": "1999-05-18",
    "description": "Digital",
    "abo": "A",
    "rhesus": "+",
    "gender": "MALE",
}

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


def test_should_status_code_ok(client):
    response = client.get('/api/')
    assert response.status_code == 200
