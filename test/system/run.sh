#!/bin/bash -Eeu

pytest \
  --capture=no \
  --color=yes \
  --ignore="${XY_APP_DIR}/test/unit" \
  --no-cov \
  -o cache_dir=/tmp \
  --pythonwarnings=error \
  --quiet \
  --random-order-bucket=global \
  --tb=short \
  --workers auto \
    "${TIDS}"
