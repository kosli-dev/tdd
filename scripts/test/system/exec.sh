#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/../lib.sh"
export_env_vars system

restart_server
wait_till_server_ready
run_tests
restart_server
gather_coverage
get_coverage
echo "${XY_HOST_COV_DIR}/index.html"
