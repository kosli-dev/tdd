#!/usr/bin/env bash
set -Eeu

docker network inspect "${XY_NETWORK}" > /dev/null \
  || docker network create --driver bridge "${XY_NETWORK}"
