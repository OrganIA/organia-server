import builtins
import inspect
import typing
from datetime import datetime

from app import errors


class Static:
    """
    Helper class for easily looking up data in dicts and converting them using
    a dataclass-like structure
    This is inspired by Pydantic and I will probably publish it as a standalone
    Python package on PyPI at some point, so I'm plugging my GitHub here:
        https://github.com/Tina-otoge/
    example:
    some_dict = {'id': '1982', 'postal_code': 12345}
    class AddressModel(Static):
        id = int
        zipcode = Model.getter('postal_code', type=str)
    address = AddressModel(some_dict)
    address.id == 1982
    address.zipcode == '12345'
    AddressModel.dict(some_dict) -> {'id': 1982, 'zipcode': '12345'}
    """

    __AUTO_STR__ = True
    __ERROR_ON_UNFOUND__ = True
    __CUSTOM_UNFOUND_RAISE__ = errors.schema_key_unfound

    @classmethod
    def _get(cls, d: builtins.dict, key):
        if cls.__ERROR_ON_UNFOUND__:
            if cls.__CUSTOM_UNFOUND_RAISE__:
                if key not in d:
                    cls.__CUSTOM_UNFOUND_RAISE__(key)
            else:
                return d[key]
        return d.get(key)

    @staticmethod
    def exists(x):
        return x is not None

    @staticmethod
    def true(x):
        return bool(x)

    @classmethod
    def getter(
        cls, key=None, type=None, cond=None, default='_none'
    ) -> typing.Callable:
        def f(d: dict, _model_key=None):
            _key = key or _model_key
            value = cls._get(d, _key)
            if type and (cond is None or cond(value)):
                value = type(value)
            elif default != '_none':
                value = default
            return value

        return f

    @staticmethod
    def const(value):
        def f(_d: dict):
            return value

        return f

    @classmethod
    def str(cls, key=None, lower=False):
        def f(x: str):
            if not x:
                return x
            x = x.strip()
            if lower:
                x = x.lower()
            return x

        return cls.getter(key=key, type=f)

    @classmethod
    def dict(cls, d: builtins.dict) -> builtins.dict:
        result = {}
        parents_keys = set()
        for parent in cls.mro()[1:-1]:
            for attr in dir(parent):
                parents_keys.add(attr)
        keys = [k for k in dir(cls) if k not in parents_keys]
        if not isinstance(d, dict):
            d = {k: getattr(d, k) for k in keys}
        for key in keys:
            type = getattr(cls, key)
            if cls.__AUTO_STR__ and type == str:
                type = cls.str()
            if not isinstance(type, typing.Type) and callable(type):
                if '_model_key' in inspect.signature(type).parameters:
                    value = type(d, _model_key=key)
                else:
                    value = type(d)
            else:
                value = type(cls._get(d, key))
            result[key] = value
        return result

    def __init__(self, d: dict):
        self.dict = self.dict(d)
        for key, value in self.dict.items():
            setattr(self, key, value)

    def __repr__(self):
        name = self.__class__.__name__
        attrs = ', '.join(
            [f'{key}={value}' for key, value in self.dict.items()]
        )
        return f'<{name} {attrs}>'

    class Timed:
        created_at = datetime
        updated_at = datetime
