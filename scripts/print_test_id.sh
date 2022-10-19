#!/usr/bin/env bash
set -Eeu

readonly LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/lib" && pwd)"
source "${LIB_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

"${LIB_DIR}/build_image.sh"

docker run \
  --entrypoint="" \
  --interactive \
  --rm \
  --tty \
  --volume="${LIB_DIR}/../../test:/${XY_DIR}/test:ro" \
  "${XY_IMAGE}" \
    "/${XY_DIR}/test/print_id.py"
