from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import config


def mount(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
