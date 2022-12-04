#!/bin/bash

if curl -s http://localhost:8000/api/ | grep "flask" > /dev/null; then
    echo Backend seems to be running, please stop it first
    exit 1
fi

rm -rf alembic/versions/*
rm data/app.db
./scripts/migrate.sh Initial migration