#!/bin/bash

if [ "$container" == "" ]; then
    python -m venv .venv
    source .venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
    pip install alembic uvicorn[standard]
fi

if [ "$NO_RELOAD" != "" ]; then
    reload_opts=''
else
    reload_opts='--reload'
fi

alembic upgrade head
uvicorn app.main:app $reload_opts --host 0.0.0.0 --port ${1:-8000}
