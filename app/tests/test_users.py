from . import assert_response, client, PREFIX
from .fixtures import clean_db


SAMPLE_USER = {
    'email': 'simple@example.com',
}


def get_users():
    response = client.get(f'{PREFIX}/users/')
    return assert_response(response, type_=list)


def create_user(data=None, **kwargs):
    data = SAMPLE_USER | (data or {}) | kwargs
    response = client.post(
        f'{PREFIX}/users/',
        json={'password': 'a'} | data
    )
    return assert_response(response, status_code=201)


def test_create_user():
    assert len(get_users()) == 1
    assert_response(create_user(), include=SAMPLE_USER)
    users = get_users()
    assert len(users) == 2
    user = users[1]
    assert_response(user, include=SAMPLE_USER)
    return user


def test_update_user():
    data = {'email': 'amazing@meatba.ll'}
    response = client.post(f'{PREFIX}/users/1', json=data)
    assert_response(response, include=data)


def test_delete_user():
    assert len(get_users()) == 1
    user = create_user()
    assert len(get_users()) == 2
    response = client.delete(f'{PREFIX}/users/{user["id"]}')
    assert_response(response)
    assert len(get_users()) == 1
