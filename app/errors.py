from werkzeug.exceptions import HTTPException as _HTTPException


def schema_key_unfound(key):
    raise InvalidRequest(f'Missing required key "{key}"')


class RaisableMixin:
    @classmethod
    def r(cls, *args, **kwargs):
        """Raises itself"""
        raise cls(*args, **kwargs)


class HTTPException(_HTTPException, RaisableMixin):
    pass


def error_handler(e: HTTPException):
    return {
        'msg': e.description,
    }, e.code


def register_error_handler(app):
    app.register_error_handler(HTTPException, error_handler)


class InternalServerError(HTTPException):
    code = 500
    description = 'An uncategorized error occurred'


class InvalidRequest(HTTPException):
    code = 422


class Unauthorized(HTTPException):
    code = 401
    description = 'Unauthorized'


class PasswordMismatchError(InvalidRequest):
    description = 'Password mismatch'


class InsufficientPermissions(Unauthorized):
    description = (
        'You do not have the required permissions to perform this action'
    )


class InvalidAuthToken(Unauthorized):
    description = 'Invalid auth token'


class AlreadyTakenError(HTTPException):
    code = 422

    def __init__(self, key, value):
        super().__init__(f'{key} "{value}" is already taken.')

    @classmethod
    def check(cls, model, column, value, filters=None):
        """Check for unique constraints

        Fast way to check if inserting a new row in table `model` with field
        `column` set to `value` will violate an unique constraint, and raise an
        error accordingly if it will, otherwise do nothing
        """
        from app import db

        query = db.session.query(model)
        if filters:
            query = query.filter(filters)
        if query.filter_by(**{column: value}).first():
            raise cls(column, value)


class NotFoundError(HTTPException):
    code = 404
    description = 'The requested resource was not found'
