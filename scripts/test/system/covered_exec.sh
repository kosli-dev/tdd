#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

if [ -z "${XY_REPO_DIR:-}" ]; then
  source "${MY_DIR}/../lib.sh"
  export $(echo_env_vars)
fi

"${MY_DIR}/lib/server_restart.sh"
wait_till_server_ready
"${MY_DIR}/lib/rm_coverage.sh"
"${MY_DIR}/lib/run_tests.sh"
"${MY_DIR}/lib/report_coverage.sh"



