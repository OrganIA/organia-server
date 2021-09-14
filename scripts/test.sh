#!/bin/bash

[ -d .venv ] && source .venv/bin/activate

code=0


pip install pytest pytest-cov requests >/dev/null
echo
echo Running pytest
echo
DB_URL='sqlite://' pytest app/tests --cov=app --cov-fail-under=90 || code=1


pip install flake8 >/dev/null
echo
echo Running flake8
echo
flake8 --statistics --show-source app || code=1


echo Exit status $code
exit $code
