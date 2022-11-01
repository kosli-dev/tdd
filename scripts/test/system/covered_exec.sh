#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

if [ -z "${XY_REPO_DIR:-}" ]; then
  source "${MY_DIR}/../lib.sh"
  export $(echo_env_vars)
fi

server_restart
wait_till_server_ready
rm_coverage system
run_tests
server_restart
report_coverage
echo "$(cov_dir system)/index.html"
