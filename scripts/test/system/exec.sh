#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/../lib.sh"
export_env_vars system

rm_coverage system
server_restart
wait_till_server_ready
run_tests
server_restart
report_coverage
echo "$(cov_dir system)/index.html"
