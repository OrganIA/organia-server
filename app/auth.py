import inspect
import flask
import functools

from app import config
from app.db.models import LoginToken, User
from app.errors import InsufficientPermissions, InvalidAuthToken


def _check(**permissions):
    PREFIX = 'Bearer '
    auth = flask.request.headers.get('Authorization')
    if not auth:
        if config.FORCE_LOGIN:
            return User.admin
        raise InvalidAuthToken("Missing Authorization header")
    if not auth.startswith(PREFIX):
        raise InvalidAuthToken(
            f"Malformed token, does not start with prefix \"{PREFIX}\""
        )
    token = auth[len(PREFIX):]
    user = LoginToken.get_from_token(token).user
    for permission, value in permissions.items():
        if not value:
            continue
        key = f'can_{permission}'
        if not hasattr(user.role, key):
            raise ValueError(f"{key} is not a valid Role permission")
        if not getattr(user.role, key):
            raise InsufficientPermissions
    return user



def check(**permissions):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = _check(**permissions)
            sig = inspect.signature(func)
            if 'auth_user' in sig.parameters:
                kwargs.setdefault('auth_user', user)
            return func(*args, **kwargs)
        return wrapper
    return decorator
