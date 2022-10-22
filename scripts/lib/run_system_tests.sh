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
  --volume="${XY_REPO_DIR}:/${XY_DIR}" \
  "${XY_IMAGE}" \
    "${XY_DIR}/test/system/run.sh"
set -e
