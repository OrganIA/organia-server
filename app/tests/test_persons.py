from . import client, PREFIX
from .fixtures import clean_db
from .helpers import assert_response


SAMPLE_PERSON = {
    'first_name': 'Test',
    'last_name': 'TEST',
    'birthday': '2021-05-13',
}


SAMPLE_PERSON_2 = {
    'first_name': 'Test2',
    'last_name': 'TEST2',
    'birthday': '2021-05-13',
}


SAMPLE_PERSON_3 = {
    'first_name': 'NoTest',
    'last_name': 'NOTEST2',
    'birthday': '2021-05-13',
}


def get_person():
    response = client.get(f'{PREFIX}/persons/')
    return assert_response(response, type_=list)


def get_person_id(id):
    response = client.get(f'{PREFIX}/persons/{id}')
    return assert_response(response, status_code=200)


def filter_name(name):
    response = client.get(f'{PREFIX}/persons/filter/{name}')
    return assert_response(response, status_code=200)


def create_person():
    response = client.post(
        f'{PREFIX}/persons/',
        json=SAMPLE_PERSON
    )
    return assert_response(response, status_code=201)


def test_create_person():
    assert len(get_person()) == 0
    assert_response(create_person(), include=SAMPLE_PERSON)
    person = get_person()
    assert len(person) == 1
    person = person[0]
    assert_response(person, include=SAMPLE_PERSON)
    return person


def test_update_person():
    person = create_person()
    data = {'first_name': 'Test0'}
    response = client.post(f'{PREFIX}/persons/{person["id"]}', json=data)
    assert_response(response, include=data)


def test_delete_person():
    assert len(get_person()) == 0
    person = create_person()
    assert len(get_person()) == 1
    response = client.delete(f'{PREFIX}/persons/{person["id"]}')
    assert_response(response)
    assert len(get_person()) == 0


def test_filter_person_name():
    # assert len(get_person()) == 0
    assert_response(create_person(), include=SAMPLE_PERSON)
    assert_response(create_person(), include=SAMPLE_PERSON_2)
    assert_response(create_person(), include=SAMPLE_PERSON_3)
    person = filter_name("Tes")
    # assert len(person) == 3
    assert_response(person, status_code=200)
