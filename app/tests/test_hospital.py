from . import client, PREFIX
from .fixtures import clean_db
from .helpers import assert_response

SAMPLE_HOSPITAL = {
    'name' : 'Robert Ballanger',
    'city_id': '1',
}


def get_hospital():
    response = client.get(f'{PREFIX}/hospital/')
    return assert_response(response, type_=list)

def get_hospital_id(id):
    response = client.get(f'{PREFIX}/hospital_id/{id}')
    return assert_response(response, status_code=200)

def create_hospital():
    response = client.post(
        f'{PREFIX}/hospital/',
        json=SAMPLE_HOSPITAL
    )
    return assert_response(response, status_code=201)


def test_create_hospital():
    assert len(get_hospital()) == 0
    assert_response(create_hospital(), include=SAMPLE_HOSPITAL)
    hospital = get_hospital()
    assert len(hospital) == 1
    hospital = hospital[0]
    assert_response(hospital, include=SAMPLE_HOSPITAL)
    return hospital