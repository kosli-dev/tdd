#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

if [ -z "${XY_LIB_DIR:-}" ]; then
  export XY_LIB_DIR="$(cd "${MY_DIR}/../../lib"; pwd)"
  source "${XY_LIB_DIR}/echo_env_vars.sh"
  export $(echo_env_vars)
fi

docker exec \
  --env TIDS="${TIDS}" \
  --interactive \
  --tty \
  "${XY_CONTAINER}" \
    "${XY_APP_DIR}/test/unit/run.sh"

echo "${XY_REPO_DIR}/test/unit/coverage/index.html"
