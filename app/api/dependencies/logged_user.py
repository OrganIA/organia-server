from fastapi import Request, Header

from app import config
from app.errors import InvalidAuthToken
from app.models import LoginToken


async def logged_user(request: Request, authorization: str = Header(None)):
    if config.FORCE_LOGIN:
        from app.models import User
        return User(email='admin')

    if authorization is None:
        raise InvalidAuthToken('Missing Authorization header')
    if hasattr(request.state, 'user'):
        return request.state.user
    PREFIX = 'Bearer '
    authorization.startswith(PREFIX) or InvalidAuthToken.r(
        f'Malformed token, does not start with prefix "{PREFIX}"'
    )
    token = LoginToken.get_from_token(authorization[len(PREFIX):])
    request.state.user = token.user
    return token.user
