#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/../lib.sh"
export_env_vars unit

rm_coverage unit

docker exec \
  --env TIDS="${TIDS}" \
  --interactive \
  "${XY_CONTAINER_NAME}" \
    "${XY_CONTAINER_DIR}/test/unit/run.sh"

tar_pipe_coverage_out unit

echo "${XY_HOST_DIR}/coverage/unit/index.html"
