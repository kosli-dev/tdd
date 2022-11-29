#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/test/lib.sh"
export $(echo_env_vars)

docker exec "${XY_CONTAINER_NAME}" \
	bash -c "pkill -SIGHUP -o gunicorn"
