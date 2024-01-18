#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/lib.sh"
export_env_vars demo

create_assets_builder
refresh_static_assets
build_image
bring_network_up

sed 's/{NAME}/demo/' "${XY_HOST_ROOT_DIR}/docker-compose.yaml" \
  | docker-compose \
    --env-file="${XY_HOST_ROOT_DIR}/env_vars/demo_up.env" \
    --file - \
      up --build --detach --force-recreate

wait_till_server_ready
open http://localhost:80