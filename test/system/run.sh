#!/bin/bash -Eeu

pytest \
  --workers auto \
  --no-cov \
  --capture=no \
  --color=yes \
  --ignore=test/unit \
  -o cache_dir=/tmp \
  --pythonwarnings=error \
  --tb=short \
  --quiet \
  --random-order-bucket=global \
    "${TIDS}"
