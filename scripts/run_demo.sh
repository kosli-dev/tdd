#!/usr/bin/env bash
set -Eeu

export LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/lib" && pwd)"
source "${LIB_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

docker rm --force "${XY_CONTAINER}" || true

docker-compose \
	--env-file=env_vars/demo_up.env \
  --file docker-compose.yaml \
    up --build --detach
