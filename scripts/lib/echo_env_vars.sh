#!/usr/bin/env bash
set -Eeu

echo_env_vars()
{
  echo XY_HOME_DIR="$(cd "${XY_LIB_DIR}/../.."; pwd)"  # in the repo
  echo XY_DIR=/xy  # in the container
  echo XY_IMAGE=xy
  echo XY_NETWORK=xy_net
  echo XY_CONTAINER=xy
  echo XY_PORT=8001
  echo XY_USER=xy
}
