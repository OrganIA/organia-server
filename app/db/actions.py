import logging
from typing import Type, Union

from app import errors
from . import session


def log(action, obj, message=None, author=None, properties=None):
    from app.models.action_log import ActionLog
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


def commit():
    session.commit()


def add(table, keys, message=None, author=None):
    obj = table(**keys)
    session.add(obj)
    session.flush()
    log(
        action='create',
        obj=obj, properties=keys,
        message=message,
        author=author
    )
    session.commit()
    return obj


def delete(obj, message=None, author=None):
    session.delete(obj)
    log(action='delete', obj=obj, message=message, author=author)
    session.commit()


def get_or_create(
    table: Type,
    search_keys: dict,
    create_keys=None,
    include_search_in_create=True,
    message=None,
    author=None,
) -> object:
    result = session.query(table).filter_by(**search_keys).first()
    print("CREATE KEYS: ", create_keys)
    print("SEARCH KEYS: ", search_keys)
    if not result:
        create_keys = create_keys or {}
        if include_search_in_create:
            # create_keys = search_keys | create_keys
            create_keys.update(search_keys)
        result = add(table, create_keys, message=message, author=author)
    return result


def get(
    table,
    filter_keys: Union[int, dict],
    error_on_unfound=None,
    unfound_error_type=errors.NotFoundError
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
