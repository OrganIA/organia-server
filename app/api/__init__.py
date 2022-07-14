import importlib
from fastapi import APIRouter

# VERSION = 'v1'
# PREFIX = f'/api/{VERSION}'
PREFIX = '/api'

ROUTERS = [
    'action_logs', 'auth', 'calendar', 'hospitals', 'info', 'listings', 'livers',
    'messages', 'messages_websockets', 'persons', 'roles', 'score', 'users',
]

api = APIRouter(prefix=PREFIX)

for name in ROUTERS:
    module = importlib.import_module(f'{__name__}.{name}')
    api.include_router(module.router)
