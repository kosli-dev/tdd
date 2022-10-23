#!/usr/bin/env bash
set -Eeu

echo_env_vars()
{
  echo XY_REPO_DIR="$(cd "${XY_LIB_DIR}/../.."; pwd)"  # Outside the container
  echo XY_APP_DIR=/xy  # Inside the container
  echo XY_CONTAINER=xy
  echo XY_IMAGE=xy_image
  echo XY_NETWORK=xy_net  # Also in docker-compose.yaml
  echo XY_PORT=8001
  echo XY_USER=xy
  echo XY_WORKERS=2
}
