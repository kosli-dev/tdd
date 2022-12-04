#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/test/lib.sh"
export_env_vars demo

docker run \
  --entrypoint="" \
  --interactive \
  --rm \
  --tty \
  --volume="${XY_HOST_ROOT_DIR}/test:${XY_CONTAINER_ROOT_DIR}/test:ro" \
  "${XY_IMAGE_NAME}" \
    "${XY_CONTAINER_ROOT_DIR}/test/print_id.py"
