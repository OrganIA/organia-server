import importlib
from fastapi import FastAPI, APIRouter
from starlette.responses import RedirectResponse

VERSION = 'v1'

app = FastAPI()
api = APIRouter(prefix=f"/api/{VERSION}")

@app.get('/')
async def index():
    return RedirectResponse(api.prefix)

for name in ['users']:
    module = importlib.import_module(f'{__name__}.{name}')
    api.include_router(module.router)

app.include_router(api)
