#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

if [ -z "${XY_REPO_DIR:-}" ]; then
  source "${MY_DIR}/../lib.sh"
  export $(echo_env_vars)
fi

server_restart
wait_till_server_ready
rm_coverage
run_tests
"${MY_DIR}/lib/report_coverage.sh"



