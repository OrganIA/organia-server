#!/bin/sh

code=0


pip install pytest requests >/dev/null
echo
echo Running pytest
echo
DB_URL='sqlite://' pytest app/tests || code=1


pip install flake8 >/dev/null
echo
echo Running flake8
echo
flake8 --statistics --show-source app || code=1


echo Exit status $code
exit $code
