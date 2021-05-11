#!/bin/bash

code=0


python -m venv .venv
./.venv/bin/pip install pytest requests >/dev/null
echo
echo Running pytest
echo
DB_URL='sqlite://' ./.venv/bin/pytest app/tests || code=1


./.venv/bin/pip install flake8 >/dev/null
echo
echo Running flake8
echo
./.venv/bin/flake8 --statistics --show-source app || code=1


echo Exit status $code
exit $code
