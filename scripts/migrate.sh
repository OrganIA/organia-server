#!/bin/bash

./.venv/bin/pip install alembic
./.venv/bin/alembic revision --autogenerate -m "$1"
