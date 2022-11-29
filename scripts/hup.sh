#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/test/lib.sh"
export_env_vars demo

docker exec "${XY_CONTAINER_NAME}" \
	bash -c "pkill -SIGHUP -o gunicorn"
