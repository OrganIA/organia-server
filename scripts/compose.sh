#!/bin/bash

docker-compose down -t 2 || podman-compose down -t 2

if [ "$1" == 'build' ]; then
	docker-compose build || podman-compose build
fi

if [[ "$1" == 'test' || "$2" == 'test' ]]; then
	docker-compose run backend ./scripts/test.sh || podman-compose run backend ./scripts/test.sh
	exit $?
fi

docker-compose up || podman-compose up
