#!/usr/bin/env bash
set -Eeu

export LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/lib" && pwd)"
source "${LIB_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

"${LIB_DIR}/build_image.sh"
"${LIB_DIR}/network_up.sh"
"${LIB_DIR}/server_up.sh"
"${LIB_DIR}/wait_till_server_ready.sh"

# "${LIB_DIR}/../exec_system_tests_with_coverage.sh"  # WIP

"${LIB_DIR}/run_system_tests.sh"  # in new container
"${LIB_DIR}/server_down.sh"
"${LIB_DIR}/wait_till_server_exited.sh"
"${LIB_DIR}/coverage_write_report.sh"

