#!/bin/sh

[ -d .venv ] && source .venv/bin/activate

alembic revision --autogenerate -m "$@"
