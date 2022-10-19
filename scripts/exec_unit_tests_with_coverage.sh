#!/usr/bin/env bash
set -Eeu

export LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/lib" && pwd)"
source "${LIB_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

docker exec \
  --env TIDS="${TIDS}" \
  --interactive \
  --tty \
  "${XY_CONTAINER}" \
    "/${XY_DIR}/test/unit/run.sh"

readonly ROOT_DIR="$(cd "${LIB_DIR}/../.." && pwd)"
echo "${ROOT_DIR}/test/unit/coverage/index.html"
