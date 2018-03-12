#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pushd ${SCRIPT_DIR} >/dev/null

# wait for mongod to initialize
sleep 10

python3 -m postprocessor
