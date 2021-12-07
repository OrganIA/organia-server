from fastapi import Request, Header

from app import config
from app import db
from app.errors import InvalidAuthToken
from app.models import LoginToken


async def logged_user(request: Request, authorization: str = Header(None)):
    if authorization is None:
        if not config.FORCE_LOGIN:
            raise InvalidAuthToken('Missing Authorization header')
        from app.models import Role, User
        return db.get_or_create(
            User,
            search_keys={'role': Role.get_admin_role()},
            create_keys={'email': 'admin@admin'},
        )
    if hasattr(request.state, 'user'):
        return request.state.user
    PREFIX = 'Bearer '
    authorization.startswith(PREFIX) or InvalidAuthToken.r(
        f'Malformed token, does not start with prefix "{PREFIX}"'
    )
    token = LoginToken.get_from_token(authorization[len(PREFIX):])
    request.state.user = token.user
    return token.user
