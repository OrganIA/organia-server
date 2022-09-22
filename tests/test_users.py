from flask.testing import FlaskClient

from tests import check


def test_perms(anon_client: FlaskClient):
    assert not check.status_ok(anon_client.get('/api/users/me'))
    assert not check.status_ok(anon_client.get('/api/users'))
    assert not check.status_ok(anon_client.get('/api/users/1'))


# def test_me(client: FlaskClient):
#     resp = client.get('/users/me')
#     assert check.status_ok(resp)
#     assert 'id' in resp.json
#     assert 'email' in resp.json
