from . import client, PREFIX
from .fixtures import clean_db
from .helpers import assert_response


SAMPLE_USER = {
    'email': 'simple@example.com',
    'name': 'simple',
}


def get_users():
    response = client.get(f'{PREFIX}/users/')
    return assert_response(response, type_=list)


def create_user():
    response = client.post(f'{PREFIX}/users/', json=SAMPLE_USER)
    return assert_response(response, status_code=201)


def test_create_user():
    assert len(get_users()) == 0
    assert_response(create_user(), include=SAMPLE_USER)
    users = get_users()
    assert len(users) == 1
    user = users[0]
    assert_response(user, include=SAMPLE_USER)
    return user


def test_update_user():
    user = create_user()
    data = {'name': 'amazing meatball'}
    response = client.post(f'{PREFIX}/users/{user["id"]}', json=data)
    assert_response(response, include=data)


def test_delete_user():
    assert len(get_users()) == 0
    user = create_user()
    assert len(get_users()) == 1
    response = client.delete(f'{PREFIX}/users/{user["id"]}')
    assert_response(response)
    assert len(get_users()) == 0
