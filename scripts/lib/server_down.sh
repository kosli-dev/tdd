#!/usr/bin/env bash
set -Eeu

docker-compose \
  --env-file=env_vars/test_system_up.env \
  --file docker-compose.yaml \
    kill -s SIGINT
