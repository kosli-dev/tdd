#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

coverage combine "${XY_DIR}"
#> /dev/null

coverage html \
  --directory "${MY_DIR}/coverage" \
  --precision=2 \
  --skip-empty
#> /dev/null
