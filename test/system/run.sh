#!/usr/bin/env bash
set -Eeu

pytest \
  --capture=no \
  --color=yes \
  --ignore="${XY_CONTAINER_ROOT_DIR}/test/unit" \
  -n auto \
  --no-cov \
  -o cache_dir=/tmp \
  --pythonwarnings=error \
  --quiet \
  --random-order-bucket=global \
  --tb=short \
    "${TIDS}"
