import sqlalchemy as sa
import json
import flask
from flask import Flask as Base
import typing
import inspect
import functools


def permissive_json(x):
    if hasattr(x, 'dict'):
        x = x.dict
    elif hasattr(x, 'to_dict'):
        x = x.to_dict
    elif (obj := sa.inspect(x, raiseerr=False)):
        return {c.key: getattr(x, c.key) for c in obj.mapper.column_attrs}
    else:
        return str(x)
    if callable(x):
        return x()
    return x


class Flask(Base):
    _deco_inject = set()
    _deco_success = set()

    def make_response(self, rv):
        code = None
        if isinstance(rv, tuple):
            code = rv[1]
            rv = rv[0]
        rv = self.response_class(
            json.dumps(rv, default=permissive_json, indent=2),
            mimetype=self.config['JSONIFY_MIMETYPE'],
            status=code,
        )
        return super().make_response(rv)

    def add_url_rule(self, rule, endpoint=None, view_func=None, provide_automatic_options=None, **options):
        view_func = self.inject(
            type=options.pop('inject_type', None),
            arg=options.pop('inject_arg', 'data'),
        )(view_func)
        view_func = self.success(options.pop('success', None))(view_func)
        return super().add_url_rule(rule, endpoint, view_func, provide_automatic_options, **options)


    @classmethod
    def inject(cls, type: typing.Callable = None, arg='data'):
        """
        Extract the JSON passed as the body to the route, and pass it as a
        parameter to the view
        :param type: Conversion to apply to the received data
        :param arg: Parameter name to use to pass the data to the view
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                sig = inspect.signature(func)
                if arg in sig.parameters and arg not in kwargs:
                    try:
                        data = json.loads(flask.request.data)
                    except json.JSONDecodeError:
                        data = {}
                    coerce = type
                    if not coerce:
                        coerce = func.__annotations__.get(arg)
                    if coerce:
                        data = coerce(data)
                    kwargs[arg] = data
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @classmethod
    def success(cls, code: int):
        """
        If the decoted view does not return a tuple, change the return value to
        a tuple with [1] being :param code:
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if not isinstance(result, tuple):
                    result = result, code
                return result
            return wrapper
        return decorator
