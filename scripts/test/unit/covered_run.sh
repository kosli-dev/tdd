#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

export XY_LIB_DIR="$(cd "${MY_DIR}/../../lib"; pwd)"
source "${MY_DIR}/../lib.sh"
export $(echo_env_vars)

"${XY_LIB_DIR}/build_image.sh"
"${XY_LIB_DIR}/network_up.sh"
"${XY_LIB_DIR}/server_up.sh"
"${XY_LIB_DIR}/wait_till_server_ready.sh"
"${MY_DIR}/covered_exec.sh"
