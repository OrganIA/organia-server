#!/bin/bash

if [ "$1" == 'build' ]; then
	docker-compose build || podman-compose build
fi

docker-compose down || podman-compose down
docker-compose up || podman-compose up
