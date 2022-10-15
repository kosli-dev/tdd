#!/usr/bin/env bash
set -Eeu

export MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${MY_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

"${MY_DIR}/build_image.sh"

docker run \
  --entrypoint="" \
  --env TIDS="${TIDS}" \
  --interactive \
  --rm \
  --tty \
  "${XY_IMAGE}" \
    /${XY_DIR}/test/unit/run.sh
