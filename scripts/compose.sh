#!/bin/bash

set -e

podman-compose down -t 2 || docker-compose down -t 2 || echo Could not down container

touch app.db

if [ "$1" == 'build' ]; then
	podman-compose build || docker-compose build
fi

if [[ "$1" == 'test' || "$2" == 'test' ]]; then
	podman-compose run backend ./scripts/test.sh || docker-compose run backend ./scripts/test.sh
	exit $?
fi

podman-compose up || docker-compose up
