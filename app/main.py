from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .api import api

app = FastAPI()


@app.get('/')
async def index():
    return RedirectResponse(api.prefix)

app.include_router(api)

from . import models
