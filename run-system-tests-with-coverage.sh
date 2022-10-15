#!/usr/bin/env bash
set -Eeu

export APP_CONTAINER=tdd
export APP_DIR=/tdd-app
export APP_IMAGE=tdd
export APP_PORT=8001
export APP_USER=tdd

export ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"${ROOT_DIR}/scripts/build_server.sh"
"${ROOT_DIR}/scripts/bring_up_server.sh"
"${ROOT_DIR}/scripts/wait_till_server_ready.sh"
"${ROOT_DIR}/scripts/run_system_tests_from_new_container.sh"
"${ROOT_DIR}/scripts/kill_server.sh"
"${ROOT_DIR}/scripts/wait_till_server_down.sh"
"${ROOT_DIR}/scripts/gather_coverage.sh"

echo "${ROOT_DIR}/test/system/coverage/index.html"
