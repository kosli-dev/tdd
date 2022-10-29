#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

if [ -z "${XY_REPO_DIR:-}" ]; then
  source "${MY_DIR}/../lib.sh"
  export $(echo_env_vars)
fi

wait_till_server_ready  # for when called from run
rm_coverage
server_restart  # start new workers

wait_till_server_ready  # new workers are ready
run_tests
server_restart  # force existing workers to exit

wait_till_server_ready
report_coverage
echo "${XY_REPO_DIR}/test/system/coverage/index.html"
