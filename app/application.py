import functools
import inspect
import json
import typing as t
from enum import Enum

import flask
from flask import Flask
from flask_cors import CORS
from pydantic import BaseModel
from sqlalchemy import orm

from app import config, db


def permissive_json(x):
    """Converts queries to list, dictable objects to dict, and functions to
    their result"""

    if isinstance(x, orm.Query):
        return x.all()
    if isinstance(x, Enum):
        return x.value.split('.')[-1]
    if hasattr(x, 'dict'):
        x = x.dict
    elif hasattr(x, 'to_dict'):
        x = x.to_dict
    else:
        return str(x)
    if callable(x):
        return x()
    return x


class App(Flask):
    """
    Subclass of Flask with our settings pre-applied, such as CORS and loading
    our config file.

    It is also customized to automatically convert all responses to JSON, and
    auto-inject schemas into routes when using type-hinting in arguments.

    ```
    class UserSchema(BaseModel):
        email: str
        password: str

    @app.post('/login')
    def login(data: UserSchema):
        assert type(data.email) == str
        assert type(data.password) == str
    ```

    You can also define response status directly in the route decorator, like so
    ```
    @app.post('/item', success=201)
    def create_item(data: dict):
        item = db.create('item', data) # pseudo-code
        return item
    ```
    Here the route will return `item` converted to JSON, and set the status code
    to 201.
    """

    def __init__(self):
        super().__init__(__name__.split('.')[0])
        CORS(self, send_wildcard=True)
        config.load_file()
        self.config['JSONIFY_MIMETYPE'] = 'application/json'
        db.init_db()

    def make_response(self, return_value):
        """The method that converts the return value of a route to a response

        We overload it to convert the return value to JSON if it's not already
        a response object.

        We also set the response code to 204 for empty responses.
        """

        code = None
        if isinstance(return_value, tuple):
            # We support returning a tuple of (data, status_code), like Flask
            code = return_value[1]
            return_value = return_value[0]
            if return_value is None:
                code = code or 204
        if not isinstance(return_value, (self.response_class, Exception)):
            if return_value is not None:
                return_value = json.dumps(
                    return_value, default=permissive_json, indent=2
                )
            return_value = self.response_class(
                return_value,
                mimetype=self.config['JSONIFY_MIMETYPE'],
                status=code,
            )
        return super().make_response(return_value)

    def add_url_rule(
        self,
        rule,
        endpoint=None,
        view_func=None,
        provide_automatic_options=None,
        **options,
    ):
        """The method that adds a route to the app

        We overload it to automatically inject schemas into the route, and
        set the response code.
        """

        view_func = self.inject(
            type=options.pop('inject_type', None),
            arg=options.pop('inject_arg', 'data'),
        )(view_func)
        view_func = self.success(options.pop('success', None))(view_func)
        return super().add_url_rule(
            rule, endpoint, view_func, provide_automatic_options, **options
        )

    @classmethod
    def inject(cls, type: t.Callable = None, arg='data'):
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
                    if isinstance(coerce, BaseModel.__class__):
                        data = coerce(**data)
                    elif coerce:
                        data = coerce(data)
                    kwargs[arg] = data
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @classmethod
    def success(cls, code: int):
        """
        If the decorated view does not return a tuple, change the return value
        to a tuple with [1] being :param code:
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
