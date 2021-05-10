#!/bin/bash

./.venv/bin/pip install alembic
./.venv/bin/alembic upgrade head
