#!/usr/bin/env bash
set -Eeu

set +e
docker run \
  --entrypoint="" \
  --env TIDS="${TIDS}" \
  --interactive \
  --net "${XY_NETWORK}" \
  --rm \
  --tty \
  --volume="${XY_REPO_DIR}:/${XY_APP_DIR}" \
  "${XY_IMAGE}" \
    "${XY_APP_DIR}/test/system/run.sh"
set -e
