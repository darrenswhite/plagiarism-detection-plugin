#!/usr/bin/env bash

docker-compose down
docker-compose up \
    --abort-on-container-exit \
    --build \
    --force-recreate \
    --remove-orphans
