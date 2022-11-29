#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/../lib.sh"
export_env_vars unit

refresh_assets
build_image
network_up
server_up
wait_till_server_ready

"${MY_DIR}/exec.sh"
