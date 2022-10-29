#!/bin/bash -Eu

cd "${XY_APP_DIR}"

coverage combine "${XY_APP_DIR}"

coverage json > /dev/null
percent=$(cat "${XY_APP_DIR}/coverage.json" | jq .totals.percent_covered)
printf "%.2f\n" "${percent}"

coverage html \
  --directory "${XY_APP_DIR}/test/system/coverage" \
  --precision=2 \
  --quiet
