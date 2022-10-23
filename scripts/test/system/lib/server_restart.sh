#!/usr/bin/env bash
set -Eeu

# There are several processes with the name gunicorn.
# One for the 'master' and one each for the workers.
# Send SIGHUP to the master which is the oldest (-o).

docker exec \
  --interactive \
  --tty \
  "${XY_CONTAINER}" \
    sh -c "pkill -SIGHUP -o gunicorn"
