#!/usr/bin/env bash
set -Eeu

export MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${MY_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

"${MY_DIR}/run_system_tests.sh"
"${MY_DIR}/coverage_write_data.sh"
"${MY_DIR}/coverage_write_report.sh"
