#!/usr/bin/env bash
set -Eeu

export MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${MY_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

"${MY_DIR}/build_image.sh"

docker run \
  --rm \
  --entrypoint="" \
  --tty \
  --interactive \
  "${XY_IMAGE}" \
    "/${XY_DIR}/test/generate_id.py"
