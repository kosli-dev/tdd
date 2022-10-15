#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "${MY_DIR}/.." && pwd)"

source "${MY_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

"${MY_DIR}/build_image.sh"

docker run \
  --entrypoint="" \
  --interactive \
  --rm \
  --tty \
  --volume="${ROOT_DIR}/test:/${XY_DIR}/test:ro" \
  "${XY_IMAGE}" \
    "/${XY_DIR}/test/print_id.py"
