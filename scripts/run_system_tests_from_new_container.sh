#!/usr/bin/env bash
set -Eeu

docker run \
  --entrypoint="" \
  --env TIDS="${TIDS}" \
  --interactive \
  --rm \
  --tty \
  "${XY_IMAGE}" \
    /${XY_DIR}/test/system/run.sh
