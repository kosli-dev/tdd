#!/usr/bin/env bash
set -Eeu

export MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "${MY_DIR}/.." && pwd)"
source "${MY_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

"${MY_DIR}/build_image.sh"
"${MY_DIR}/server_up.sh"
"${MY_DIR}/wait_till_server_ready.sh"

docker exec \
  --env TIDS="${TIDS}" \
  --interactive \
  --tty \
  "${XY_CONTAINER}" \
    "/${XY_DIR}/test/unit/run.sh"

echo "${ROOT_DIR}/test/unit/coverage/index.html"
