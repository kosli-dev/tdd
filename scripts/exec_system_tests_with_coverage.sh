#!/usr/bin/env bash
set -Eeu

export LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/lib" && pwd)"
source "${LIB_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

"${LIB_DIR}/coverage_rm.sh"
"${LIB_DIR}/run_system_tests.sh"
"${LIB_DIR}/coverage_report.sh"
#"${LIB_DIR}/coverage_write_report.sh"
