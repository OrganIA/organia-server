from werkzeug.wrappers.response import Response


def status_ok(x):
    if isinstance(x, Response):
        x = x.status_code
    if x == 404:
        raise Exception('Got a 404')
    return x >= 200 and x <= 299
