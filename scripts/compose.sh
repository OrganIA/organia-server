#!/bin/bash

docker-compose down || podman-compose down
docker-compose up || podman-compose up
