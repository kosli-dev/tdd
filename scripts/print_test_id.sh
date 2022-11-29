#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/test/lib.sh"
export $(echo_env_vars)

docker run \
  --entrypoint="" \
  --interactive \
  --rm \
  --tty \
  --volume="${XY_REPO_DIR}/test:${XY_APP_DIR}/test:ro" \
  "${XY_IMAGE_NAME}" \
    "${XY_APP_DIR}/test/print_id.py"
