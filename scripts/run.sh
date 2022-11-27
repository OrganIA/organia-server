#!/bin/bash

if [ "$container" == "" ]; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
fi

if [ "$NO_RELOAD" != "" ]; then
    reload_opts=''
else
    reload_opts='--reload'
fi

alembic upgrade head
export PORT=${1:-8000}
FLASK_RUN_HOST=0.0.0.0 FLASK_RUN_PORT=$PORT flask run $reload_opts
