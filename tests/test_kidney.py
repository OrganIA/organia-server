data = {
    "person_id": 1,
    "hospital_id": 1,
    "start_date": "2022-12-05",
    "weight_kg": "60",
    "height_cm": "20",
    "re_registration_date": "2022-12-05",
    "transplantation_date": "2022-12-05",
    "notes": "notes",
    "type": "RECEIVER",
    "organ_type": "KIDNEY",
    "organ": {
        "A": 1,
        "B": 110,
        "C": 10,
        "DR": 10,
        "DQ": 0,
        "dialysis_end_date": "2022-12-05",
        "dialysis_start_date": "2022-12-05",
        "is_under_dialysis": True,
        "is_dialyse": True,
        "is_retransplantation": False,
        "start_date_dialyse": "2022-12-12",
        "arf_date": "2022-12-12",
        "date_transplantation": "2022-12-12",
        "re_registration_date": "2022-12-12",
    },
    "person": {
        "first_name": "saber",
        "last_name": "saber",
        "birth_date": "2022-12-05",
        "description": "agile et nerveux",
        "abo": "A",
        "rhesus": "+",
        "gender": "OTHER",
    },
}

data_kidney_invalid = {
    "person_id": 1,
    "hospital_id": 1,
    "start_date": "2022-12-05",
    "weight_kg": "60",
    "height_cm": "20",
    "re_registration_date": "2022-12-05",
    "transplantation_date": "2022-12-05",
    "notes": "notes",
    "type": "RECEIVER",
    "organ_type": "KIDNEY",
    "organ": {
        "is_dialyse": True,
    },
}


def test_should_status_code_ok(client):
    response = client.get('/api/')
    assert response.status_code == 200


def test_create_kidney(client):
    response = client.post('/api/listings/', json=data)
    assert response.status_code == 200


def test_create_kidney_invalid(client):
    response = client.post('/api/listings/', json=data_kidney_invalid)
    assert response.status_code == 422
