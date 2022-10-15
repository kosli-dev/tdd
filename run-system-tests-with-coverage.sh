#!/usr/bin/env bash
set -Eeu

export XY_CONTAINER=tdd
export XY_DIR=tdd-app
export XY_IMAGE=tdd
export XY_PORT=8001
export XY_USER=tdd

export ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"${ROOT_DIR}/scripts/build_server.sh"
"${ROOT_DIR}/scripts/bring_up_server.sh"
"${ROOT_DIR}/scripts/wait_till_server_ready.sh"
"${ROOT_DIR}/scripts/run_system_tests_from_new_container.sh"
"${ROOT_DIR}/scripts/kill_server.sh"
"${ROOT_DIR}/scripts/wait_till_server_down.sh"
"${ROOT_DIR}/scripts/gather_coverage.sh"

echo "${ROOT_DIR}/test/system/coverage/index.html"
