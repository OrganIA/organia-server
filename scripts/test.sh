#!/bin/bash

python -m venv .venv
./.venv/bin/pip install pytest requests
./.venv/bin/pytest -s
