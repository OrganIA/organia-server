from app import app
from werkzeug.exceptions import HTTPException


@app.errorhandler(HTTPException)
def error_handler_http(e: HTTPException):
    return {
        'msg': e.description,
    }, e.code


# @app.errorhandler(Exception)
# def error_handler(e: Exception):
#     return error_handler_http(HTTPException(str(e), code=500))


class HTTPException(HTTPException):
    def __init__(self, detail=None, code=None):
        self.code = code
        super().__init__(description=detail)


class RaisableMixin:
    @classmethod
    def r(cls, *args, **kwargs):
        """Raises itself"""
        raise cls(*args, **kwargs)


class InvalidRequest(RaisableMixin, HTTPException):
    def __init__(self, msg=None):
        super().__init__(code=422, detail=msg)


class Unauthorized(RaisableMixin, HTTPException):
    DEFAULT = None

    def __init__(self, msg=None):
        super().__init__(code=401, detail=msg or self.DEFAULT)


class InsufficientPermissions(Unauthorized):
    DEFAULT = 'You do not have the required permissions to perform this action'


class InvalidAuthToken(Unauthorized):
    DEFAULT = 'Invalid auth token'


class AlreadyTakenError(HTTPException):
    def __init__(self, key, value):
        super().__init__(
            code=422, detail=f'{key} "{value}" is already taken.'
        )

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


class NotFoundError(RaisableMixin, HTTPException):
    def __init__(self, msg=None):
        super().__init__(code=404, detail=msg or 'Not found.')


class PasswordMismatchError(HTTPException):
    def __init__(self, msg=None):
        super().__init__(code=401, detail=msg or 'Password mismatch.')


class NotAcceptableError(HTTPException):
    def __init__(self, msg=None):
        super().__init__(code=406, detail=msg or 'Not Acceptable.')
