# from flask.testing import FlaskClient

# from tests import check


# def test_register_invalid_params(anon_client: FlaskClient):
#     resp = anon_client.post('/api/auth/register')
#     assert not check.status_ok(resp)
#     resp = anon_client.post(
#         '/api/auth/register', json={'email': 'only@email.com'}
#     )
#     assert not check.status_ok(resp)
#     resp = anon_client.post(
#         '/api/auth/register', json={'password': 'only password'}
#     )
#     assert not check.status_ok(resp)


# def test_register(anon_client: FlaskClient):
#     resp = anon_client.post(
#         '/api/auth/register',
#         json={'email': 'good@email.com', 'password': 'good password'},
#     )
#     assert check.status_ok(resp)
#     assert resp.json['token']
