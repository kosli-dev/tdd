#!/usr/bin/env bash
set -Eeu

cd "${XY_REPO_DIR}"

docker-compose \
  --env-file=env_vars/test_system_up.env \
  --file docker-compose.yaml \
    kill -s SIGINT
