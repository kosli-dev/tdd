#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "${MY_DIR}/.." && pwd)"

docker exec \
  --interactive \
  --tty \
  "${XY_CONTAINER}" \
    "/${XY_DIR}/test/system/stop_coverage.py"

