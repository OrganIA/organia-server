#!/bin/bash

set -e

touch app.db

podman-compose down -t 2 || echo Could not down container

if [ "$1" == 'build' ]; then
	docker-compose build
fi

if [[ "$1" == 'test' || "$2" == 'test' ]]; then
	podman-compose run backend ./scripts/test.sh
	exit $?
fi

podman-compose up
