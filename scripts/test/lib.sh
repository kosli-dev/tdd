#!/usr/bin/env bash
set -Eeu

echo_env_vars() {
  echo XY_REPO_DIR="$(cd "${XY_LIB_DIR}/../.."; pwd)"  # Outside the container
  echo XY_APP_DIR=/xy  # Inside the container
  echo XY_CONTAINER=xy
  echo XY_IMAGE=xy_image
  echo XY_NETWORK=xy_net  # Also in docker-compose.yaml
  echo XY_PORT=8001
  echo XY_USER=xy
  echo XY_WORKERS=2
}

build_image() {
  cd "${XY_REPO_DIR}"
  docker build \
    --build-arg XY_APP_DIR \
    --build-arg XY_PORT \
    --build-arg XY_USER \
    --build-arg XY_WORKERS \
    --file Dockerfile \
    --tag "${XY_IMAGE}" \
      .
}

network_up() {
  docker network inspect "${XY_NETWORK}" > /dev/null \
    || docker network create --driver bridge "${XY_NETWORK}"
}

server_up() {
  cd "${XY_REPO_DIR}"
  docker-compose \
    --env-file=env_vars/test_system_up.env \
    --file docker-compose.yaml \
      up --no-build --detach
}
