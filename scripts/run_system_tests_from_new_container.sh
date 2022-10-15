#!/usr/bin/env bash
set -Eeu

docker run \
  --entrypoint="" \
  --interactive \
  --rm \
  --tty \
  "${XY_IMAGE}" \
    /${XY_DIR}/test/system/run.sh
