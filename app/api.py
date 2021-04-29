import importlib
from fastapi import APIRouter

VERSION = 'v1'
PREFIX = f'/api/{VERSION}'

api = APIRouter(prefix=PREFIX)

for name in ['users']:
    module = importlib.import_module(f'app.{name}')
    api.include_router(module.router)
