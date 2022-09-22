import logging
from typing import Type, Union

from app import errors

from . import session


def log(
    action, obj, message=None, author=None, properties=None, session=session
):
    from app.db.models.action_log import ActionLog

    log = ActionLog(
        action=action,
        target_type=type(obj).__name__,
        target_id=getattr(obj, 'id'),
        properties=str(properties),
        message=message,
        author=author,
    )
    session.add(log)
    session.commit()
    logging.info(str(log))


def commit(session=session):
    session.commit()


def add(table, keys, message=None, author=None, session=session):
    obj = table(**keys)
    session.add(obj)
    session.flush()
    # log(
    #     action='create',
    #     obj=obj,
    #     properties=keys,
    #     message=message,
    #     author=author,
    # )
    session.commit()
    return obj


def delete(obj, message=None, author=None, session=session):
    session.delete(obj)
    log(action='delete', obj=obj, message=message, author=author)
    session.commit()


class Action:
    created = False

    @classmethod
    @property
    def fetched(cls):
        return not cls.created

    @classmethod
    def fetch(cls):
        cls.created = False

    @classmethod
    def create(cls):
        cls.created = True


def get_or_create(
    table: Type,
    keys: dict = None,
    filter_keys: list = None,
    session=session,
    action=Action,
    **extra_keys,
) -> object:
    keys = keys or {}
    keys |= extra_keys
    filter_keys = filter_keys or keys.keys()
    search_keys = {k: keys[k] for k in filter_keys}
    result = session.query(table).filter_by(**search_keys).first()
    if not result:
        result = add(table, keys, session=session)
        action.create()
    else:
        action.fetch()
    return result


def get(
    table,
    filter_keys: Union[int, dict],
    error_on_unfound=None,
    unfound_error_type=errors.NotFoundError,
    session=session,
):
    if error_on_unfound is None:
        error_on_unfound = isinstance(filter_keys, int)
    if isinstance(filter_keys, int):
        result = session.get(table, filter_keys)
    else:
        result = session.query(table).filter_by(**filter_keys).first()
    if result is None and error_on_unfound:
        raise unfound_error_type(
            f'Could not find a {table.__name__} when searching {filter_keys}'
        )
    return result


def edit(obj, new_values: dict, author=None, message=None):
    for key, value in new_values.items():
        if not hasattr(obj, key):
            raise ValueError(f'Object {obj} does not have a property {key}')
        setattr(obj, key, value)
    log(
        action='edit',
        obj=obj,
        message=message,
        author=author,
        properties=new_values,
    )
    session.commit()
