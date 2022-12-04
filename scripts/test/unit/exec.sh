#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/../lib.sh"
export_env_vars unit

run_tests unit
tar_pipe_coverage_out unit
echo "${XY_HOST_COV_DIR}"
