#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "${MY_DIR}/../.." && pwd)"

set +e
docker run \
  --entrypoint="" \
  --env TIDS="${TIDS}" \
  --interactive \
  --net "${XY_NETWORK}" \
  --rm \
  --tty \
  --volume="${ROOT_DIR}:/${XY_DIR}" \
  "${XY_IMAGE}" \
    "/${XY_DIR}/test/system/run.sh"
set -e
