from app.errors import InsufficientPermissions


def check(value: bool, msg=None):
    if not value:
        raise InsufficientPermissions(msg)


from . import roles, users