#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

if [ -z "${XY_LIB_DIR:-}" ]; then
  export XY_LIB_DIR="$(cd "${MY_DIR}/../../lib"; pwd)"
  source "${XY_LIB_DIR}/echo_env_vars.sh"
  export $(echo_env_vars)
fi

"${MY_DIR}/lib/server_restart.sh"
"${XY_LIB_DIR}/wait_till_server_ready.sh"
"${MY_DIR}/lib/rm_coverage.sh"
"${MY_DIR}/lib/run_tests.sh"
"${MY_DIR}/lib/report_coverage.sh"



