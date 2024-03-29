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


def check(**perms):
    need_user(**perms)


def need_user(**perms):
    if flask.request.method == 'OPTIONS':
        return None
    user = _retrieve_user()
    for perm in perms:
        if not getattr(user.role, f"can_{perm}"):
            raise InsufficientPermissions(
                f"You need the permission {perm} to access this route"
            )
    return user


def route(**perms):
    """
    Decorator to require authentication on a route.

    Use `@auth.route()` to simply require a valid auth token.
    Use `@auth.route(perm1=True, perm2=True)` to also validate against perms.

    If the route has a parameter named `auth_user`, the current user will be
    injected as this parameter.

    ```
    @app.get('/')
    @auth.routeui()
    def index():
        ...

    @app.get('/admin')
    @auth.route(edit_users=True)
    def admin(auth_user: User):
        print(f"{auth_user} just accessed the admin page!")
    ```
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = need_user(**perms)
            sig = inspect.signature(func)
            if 'auth_user' in sig.parameters:
                kwargs.setdefault('auth_user', user)
            return func(*args, **kwargs)

        return wrapper

    return decorator
