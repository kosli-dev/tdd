#!/usr/bin/env bash
set -Eeu

docker run \
  --entrypoint="" \
  --interactive \
  --rm \
  --tty \
  "${APP_IMAGE}" \
    /${APP_DIR}/test/system/run.sh
