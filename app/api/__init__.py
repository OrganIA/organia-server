import importlib
from fastapi import APIRouter

VERSION = 'v1'
PREFIX = f'/api/{VERSION}'
ROUTERS = ['users']

api = APIRouter(prefix=PREFIX)

for name in ROUTERS:
    module = importlib.import_module(f'{__name__}.{name}')
    api.include_router(module.router)