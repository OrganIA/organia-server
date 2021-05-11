def get_or_404(*args, **kwargs):
    """Calls sqlalchemy.session.get and raises a 404 if nothing is found"""
    from app.errors import NotFoundError
    from . import session
    result = session.get(*args, **kwargs)
    if result is None:
        raise NotFoundError
    return result
