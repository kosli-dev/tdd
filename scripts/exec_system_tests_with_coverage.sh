#!/usr/bin/env bash
set -Eeu

if [ -z "${XY_LIB_DIR:-}" ]; then
  export XY_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/lib"; pwd)"
  source "${XY_LIB_DIR}/echo_env_vars.sh"
  export $(echo_env_vars)
fi

"${XY_LIB_DIR}/coverage_rm.sh"

# Do I need to wait for the old gunicorns to exit?
"${XY_LIB_DIR}/wait_till_server_ready.sh"

"${XY_LIB_DIR}/run_system_tests.sh"

# If there is more than one worker this CURL will only reach one of them...
"${XY_LIB_DIR}/coverage_report.sh"

# Do the restart here so next est wait-till-server-ready is quick
"${XY_LIB_DIR}/server_restart.sh"



