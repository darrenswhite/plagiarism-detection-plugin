#!/usr/bin/env bash

set -x

function initiate() {
    # wait for mongod
    sleep 5

    # check if replica set is initialized
    status=$(mongo --eval 'rs.status()' | grep -q "NotYetInitialized")
    if [ $? -eq 0 ]; then
        # initialise replica set
        mongo --eval 'rs.initiate()';
    fi
}

# do replica set initialization in the background
initiate &

# run mongod as a replica set
mongod --bind_ip 0.0.0.0 --smallfiles --replSet rs0
