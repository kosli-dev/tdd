#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "${MY_DIR}/.." && pwd)"

docker run \
  --entrypoint="" \
  --env TIDS="${TIDS}" \
  --interactive \
  --name xy_system_test_runner \
  --net "${XY_NETWORK}" \
  --rm \
  --tty \
  --volume="${ROOT_DIR}/test:/${XY_DIR}/test" \
  "${XY_IMAGE}" \
    /${XY_DIR}/test/system/run.sh
