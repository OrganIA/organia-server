import importlib
import logging
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .api import api
from .logger import WebhookHandler
from . import config


MIDDLEWARES = ['cors']

app = FastAPI()

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[WebhookHandler(config.DISCORD_LOGS)],
)


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
