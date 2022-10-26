#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/test/lib.sh"
export $(echo_env_vars)

build_image

docker rm --force "${XY_CONTAINER}" 2> /dev/null || true

cd "${XY_REPO_DIR}"

docker-compose \
	--env-file=env_vars/demo_up.env \
  --file docker-compose.yaml \
    up --build --detach
