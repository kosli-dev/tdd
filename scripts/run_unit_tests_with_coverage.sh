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
  --volume="${MY_DIR}/../test:/${XY_DIR}/test" \
  "${XY_IMAGE}" \
    /${XY_DIR}/test/unit/run.sh

readonly ROOT_DIR="$(cd "${MY_DIR}/.." && pwd)"
echo "open ${ROOT_DIR}/test/unit/coverage/index.html"
