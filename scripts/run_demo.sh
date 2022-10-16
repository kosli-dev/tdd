#!/usr/bin/env bash
set -Eeu

export MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${MY_DIR}/echo_env_vars.sh"
export $(echo_env_vars)

docker rm --force "${XY_CONTAINER}" || true

docker-compose \
	--env-file=env_vars/test_system_up.env \
  --file docker-compose.yaml \
    up --build --detach
