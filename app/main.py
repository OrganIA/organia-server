import importlib
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .api import api


MIDDLEWARES = ['cors']

app = FastAPI()


for name in MIDDLEWARES:
    module = importlib.import_module(f'app.{name}')
    module.mount(app)


@app.get('/')
async def index():
    return RedirectResponse(api.prefix)


"""
FIXME deprecation warning
@app.middleware('http')
async def return_204_for_empty_response(request: Request, call_next):
    with warnings.catch_warnings():
        response = await call_next(request)
        if (
            response.status_code < 300
            # TODO: check if actually empty instead
            and int(response.headers['content-length']) == len('null')
        ):
            response.status_code = 204
        return response
"""

app.include_router(api)
