#!/usr/bin/env bash
set -Eeu

docker build \
  --build-arg XY_DIR \
  --build-arg XY_PORT \
  --build-arg XY_USER \
  --file Dockerfile \
  --tag "${XY_IMAGE}" \
    .
