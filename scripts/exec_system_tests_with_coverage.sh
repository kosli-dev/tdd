#!/usr/bin/env bash
set -Eeu

if [ -z "${XY_LIB_DIR:-}" ]; then
  export XY_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/lib"; pwd)"
  source "${XY_LIB_DIR}/echo_env_vars.sh"
  export $(echo_env_vars)
fi

"${XY_LIB_DIR}/server_restart.sh"
"${XY_LIB_DIR}/wait_till_server_ready.sh"
"${XY_LIB_DIR}/coverage_rm.sh"
"${XY_LIB_DIR}/run_system_tests.sh"
"${XY_LIB_DIR}/coverage_reports.sh"



