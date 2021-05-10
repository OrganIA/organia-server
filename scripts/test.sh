#!/bin/bash

code=0


python -m venv .venv
./.venv/bin/pip install pytest requests
./.venv/bin/pytest -s app/tests || code=1


./.venv/bin/pip install flake8
./.venv/bin/flake8 --statistics --show-source app || code=1


echo Exit status $code
exit $code
