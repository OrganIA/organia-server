from app import db
from app.models import User
from . import assert_response, client, PREFIX, test_users
from .fixtures import clean_db


USER = {
    'email': 'login@testi.com',
}

PASSWORD = 'lets gooooooo'

USER_PW = {
    **USER,
    'password': PASSWORD,
}


def test_password_is_hashed():
    user = test_users.create_user(USER_PW)
    user = db.session.get(User, user['id'])
    assert user.password != PASSWORD


def test_login_correct():
    test_users.create_user(USER_PW)
    response = client.post(f'{PREFIX}/auth/', json={
        'email': USER['email'], 'password': PASSWORD,
    })
    data = assert_response(response, status_code=200)
    assert 'token' in data
    assert isinstance(data['token'], str)
    assert_response(data['user'], include=USER)


def test_login_incorrect_password():
    test_users.create_user(USER_PW)
    response = client.post(f'{PREFIX}/auth/', json={
        'email': USER['email'], 'password': 'something else',
    })
    assert_response(response, status_code=401)


def test_login_unexisting_user():
    response = client.post(f'{PREFIX}/auth/', json={
        'email': USER['email'], 'password': 'something else',
    })
    assert_response(response, status_code=422)
