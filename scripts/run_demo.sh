#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/test/lib.sh"
export_env_vars demo

refresh_assets
build_image

cat ${XY_REPO_DIR}/docker-compose.yaml | sed 's/{NAME}/demo/' \
  | docker-compose \
    --env-file="${XY_REPO_DIR}/env_vars/demo_up.env" \
    --file - \
      up --build --detach --force-recreate

wait_till_server_ready