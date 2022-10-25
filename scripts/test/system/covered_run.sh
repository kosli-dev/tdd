#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

export XY_LIB_DIR="$(cd "${MY_DIR}/../../lib"; pwd)"
source "${MY_DIR}/../lib.sh"
export $(echo_env_vars)

build_image
network_up
server_up
wait_till_server_ready

"${MY_DIR}/covered_exec.sh"
