#!/bin/bash

[ -d .venv ] && source .venv/bin/activate

code=0

export PYTHONPATH=.


pip install pytest flask-sqlalchemy pytest-cov requests >/dev/null
echo
echo Running pytest
echo
DB_URL='sqlite://' FORCE_LOGIN=1 pytest tests --cov=app --cov-fail-under=90
last=$?

# echo -n "Unit tests + coverage: "
# if [ $last == 0 ]; then
# 	echo OK
# else
# 	code=1
# 	echo FAIL
# fi


pip install flake8 >/dev/null
echo
echo Running flake8
echo
flake8 --statistics --show-source app
last=$?

echo -n "Coding style: "
if [ $last == 0 ]; then
	echo OK
else
	code=1
	echo FAIL
fi


echo
echo
echo Exit status $code
exit $code
