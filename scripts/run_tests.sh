#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/lib.sh"
export_env_vars "${1}"

refresh_static_assets
build_image
bring_network_up
bring_server_up
exec_tests_get_coverage
