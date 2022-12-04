#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/../lib.sh"
export_env_vars system

refresh_static_assets
build_image
bring_network_up
bring_server_up
wait_till_server_ready
exec_tests_get_coverage
