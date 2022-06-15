import flask
from flask_cors import CORS
import functools
import inspect
import json
from sqlalchemy import orm
import typing

from app import config


def permissive_json(x):
    if isinstance(x, orm.Query):
        return x.all()
    if hasattr(x, 'dict'):
        x = x.dict
    elif hasattr(x, 'to_dict'):
        x = x.to_dict
    else:
        return str(x)
    if callable(x):
        return x()
    return x


class App(flask.Flask):
    """
    Subclass of Flask with out settings pre-applied, such as CORS and loading
    our config file.

    It is also customized to automatically convert all responses to JSON, and
    auto-inject schemas into routes when using type-hinting in arguments.

    ```
    class UserSchema(Static):
        email = str
        password = str

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
        CORS(self)
        config.load_file()

    def make_response(self, rv):
        code = None
        if isinstance(rv, tuple):
            code = rv[1]
            rv = rv[0]
        if not isinstance(rv, (self.response_class, Exception)):
            if rv is None:
                code = code or 204
            else:
                rv = json.dumps(rv, default=permissive_json, indent=2)
            rv = self.response_class(
                rv,
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
