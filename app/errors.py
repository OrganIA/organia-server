from fastapi import HTTPException

class AlreadyTakenError(HTTPException):
    def __init__(self, key, value):
        super().__init__(
            status_code=422, detail=f'{key} "{value}" is already taken.'
        )

    @classmethod
    def check(cls, model, column, value):
        """Check for unique constraints

        Fast way to check if inserting a new row in table `model` with field
        `column` set to `value` will violate an unique constraint, and raise an
        error accordingly if it will, otherwise do nothing
        """
        from app import db
        if db.session.query(model).filter_by(**{column: value}).first():
            raise cls(column, value)
