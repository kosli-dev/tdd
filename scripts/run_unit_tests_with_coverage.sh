#!/usr/bin/env bash
set -Eeu

export MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${MY_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

"${MY_DIR}/build_image.sh"
"${MY_DIR}/server_up.sh"
"${MY_DIR}/wait_till_server_ready.sh"
"${MY_DIR}/exec_unit_tests_with_coverage.sh"
