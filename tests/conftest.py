"""
refs:
    https://flask.palletsprojects.com/en/2.2.x/tutorial/tests/
    https://flask.palletsprojects.com/en/2.2.x/testing/
"""

import pytest

from app import create_app, db


@pytest.fixture(scope='function', autouse=True)
def app():
    app = create_app(test=True)

    yield app

    db.engine = None


@pytest.fixture()
def anon_client(app):
    return app.test_client()


class AuthActions:
    DEFAULT_EMAIL = 'test@test.com'
    DEFAULT_PASSWORD = 'test'

    def __init__(self, client):
        self._client = client
        self.token = self.register()

    def login(self, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD):
        return self._client.post(
            '/api/login',
            data={'email': email, 'password': password},
        )

    def register(self, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD):
        return self._client.post(
            '/api/register',
            data={'email': email, 'password': password}
        )


@pytest.fixture
def auth_client(anon_client):
    return AuthActions(anon_client)

"""
Attempt without using Flask.test_client
"""
# class Client(Session):
#     def __init__(self, app: Flask, *args, prefix=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._token = None
#         app.env
#         self.base = 'http://127.0.0.1' + f':{config.PORT}'
#         self.prefix = prefix

#     def request(self, method, url, *args, **kwargs):
#         if url.startswith('/'):
#             base = self.base
#             if self.prefix:
#                 base += self.prefix
#             url = base + url
#         return super().request(method, url, *args, **kwargs)



# class AuthClient(Client):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         resp = self.post('/api/auth/register', json={
#             'email': 'test@email.com',
#             'password': 'test password',
#         })
#         assert resp.json
#         self._token = resp.json['token']

#     def request(self, *args, **kwargs):
#         if self._token:
#             headers = kwargs.get('headers') or {}
#             headers.setdefault('Authorization', f'Bearer: {self._token}')
#             kwargs['headers'] = headers
#         return super().request(*args, **kwargs)


# @pytest.fixture()
# def anon_client(app: Flask):
#     return Client(app, prefix='/api')


# @pytest.fixture()
# def client(app: Flask):
#     return AuthClient(app, prefix='/api')
