#!/usr/bin/env bash
set -Eeu

docker exec \
  --interactive \
  --tty \
  "${XY_CONTAINER}" \
    sh -c "pkill -SIGHUP -o gunicorn"
