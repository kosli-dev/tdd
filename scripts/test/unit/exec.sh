#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/../lib.sh"
export_env_vars unit

rm_coverage unit

docker exec \
  --env TIDS="${TIDS}" \
  --interactive \
  --tty \
  "${XY_CONTAINER_NAME}" \
    "${XY_APP_DIR}/test/unit/run.sh"

echo "${XY_REPO_DIR}/coverage/unit/index.html"
