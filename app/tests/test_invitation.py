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

def get_invitations():
    response = client.get(f'{PREFIX}/invitations/')
    return assert_response(response, type_=list)


def create_user():
    response = client.post(
        f'{PREFIX}/create_user/',
        json=SAMPLE_USER | {'password': 'a'}
    )
    return assert_response(response, status_code=201)

def create_invitation():
    response = client.post(
        f'{PREFIX}/create_invitation/',
        json=SAMPLE_USER | {'invite_token': 'a'}
    )
    return assert_response(response, status_code=201)


def test_create_invitation():
    assert len(get_users()) == 0
    assert_response(create_invitation(), include=SAMPLE_USER)
    invitations = get_invitations()
    assert len(invitations) == 1
    invitation = invitations[0]
    assert_response(invitation, include=SAMPLE_USER)
    return invitation