#!/usr/bin/env bash
set -Eeu

cd "${XY_HOME_DIR}"

docker-compose \
	--env-file=env_vars/test_system_up.env \
  --file docker-compose.yaml \
    up --no-build --detach
