#!/usr/bin/env bash
set -Eeu

docker build \
  --file Dockerfile \
  --build-arg APP_DIR \
  --build-arg APP_PORT \
  --build-arg APP_USER \
  --tag "${APP_IMAGE}" \
    .
