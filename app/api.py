import importlib
from fastapi import APIRouter

VERSION = 'v1'

api = APIRouter(prefix=f"/api/{VERSION}")

for name in ['users']:
    module = importlib.import_module(f'app.{name}')
    api.include_router(module.router)
