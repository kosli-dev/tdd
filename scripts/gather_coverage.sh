#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "${MY_DIR}/.." && pwd)"

docker run \
  --entrypoint="" \
  --interactive \
  --net "${XY_NETWORK}" \
  --rm \
  --tty \
  --volume="${ROOT_DIR}/test:/${XY_DIR}/test" \
  "${XY_IMAGE}" \
    /${XY_DIR}/test/system/gather_coverage.sh

echo "open ${ROOT_DIR}/test/system/coverage/index.html"
