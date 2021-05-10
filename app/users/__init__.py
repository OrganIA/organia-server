from fastapi import APIRouter

router = APIRouter(prefix='/users')


from . import models, routes
