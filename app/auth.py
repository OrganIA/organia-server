import functools
import inspect

import flask

from app import config
from app.db.models import LoginToken, User
from app.errors import InsufficientPermissions, InvalidAuthToken

PREFIX = 'Bearer '


def _retrieve_user():
    auth = flask.request.headers.get('Authorization')
    if not auth:
        if config.FORCE_LOGIN:
            return User.admin
        raise InvalidAuthToken("Missing Authorization header")
    if not auth.startswith(PREFIX):
        raise InvalidAuthToken(
            f"Malformed token, does not start with prefix \"{PREFIX}\""
        )

    token = auth[len(PREFIX) :]
    user = LoginToken.get_from_token(token).user
    return user


def check(admin=False):
    need_user(admin=admin)


def need_user(admin=False):
    if flask.request.method == 'OPTIONS':
        return None
    user = _retrieve_user()
    if admin and not user.is_admin:
        raise InsufficientPermissions(
            "You must be an admin to access this route"
        )
    return user


def route(admin=False):
    """
    Decorator to require authentication on a route.

    Use `@auth.route()` to simply require a valid auth token.
    Use `@auth.route(admin=True)` to also validate against admin perms.

    If the route has a parameter named `auth_user`, the current user will be
    injected as this parameter.

    ```
    @app.get('/')
    @auth.route()
    def index():
        ...

    @app.get('/admin')
    @auth.route(admin=True)
    def admin(auth_user: User):
        print(f"{auth_user} just accessed the admin page!")
    ```
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = need_user(admin=admin)
            sig = inspect.signature(func)
            if 'auth_user' in sig.parameters:
                kwargs.setdefault('auth_user', user)
            return func(*args, **kwargs)

        return wrapper

    return decorator
