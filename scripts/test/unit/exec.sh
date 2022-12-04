#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/../lib.sh"
export_env_vars unit

run_tests
get_coverage
echo "${XY_HOST_COV_DIR}/index.html"
