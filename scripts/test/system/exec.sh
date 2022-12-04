#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/../lib.sh"
export_env_vars system

server_restart
wait_till_server_ready
run_tests
server_restart
gather_coverage
tar_pipe_coverage_out
echo "${XY_HOST_COV_DIR}/index.html"
