import importlib
import logging
from fastapi import FastAPI
from starlette.requests import Request
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


@app.get('/test/{module}')
async def test(module):
    module = importlib.import_module(f'app.{module}')
    return module.test()


@app.on_event('startup')
async def create_basic_roles():
    from app.models import Role
    Role.setup_roles()


@app.middleware('http')
async def log_each_request(request: Request, call_next):
    from . import logger
    logger.info(
        'Got %s %s %s',
        request.method,
        request.url,
        (await request.body()).decode(),
    )
    return await call_next(request)

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
