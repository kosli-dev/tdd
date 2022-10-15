#!/usr/bin/env bash
set -Eeu

docker build \
  --file Dockerfile \
  --build-arg XY_DIR \
  --build-arg XY_PORT \
  --build-arg XY_USER \
  --tag "${XY_IMAGE}" \
    .
