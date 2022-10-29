#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Important to _not_ quote the rm'd expression here so * expands
rm ${XY_APP_DIR}/.coverage* > /dev/null || true
#rm -rf "${XY_APP_DIR}/test/unit/coverage" > /dev/null || true

set +e
# To set the random-ordering seed
#       --random-order-seed=<seed>
pytest \
  --cache-clear `# Clear .coverage cache. It persists as it is in the volume-mount` \
  --capture=no `# Turn off capturing. Makes print() effects visible and interleaved` \
  --color=yes \
  --cov="${XY_APP_DIR}/server/" \
  --cov-config="${MY_DIR}/.coveragerc" \
  --cov-report= `# Turn off verbose coverage report` \
  --ignore=test/system \
  --pythonwarnings=error \
  --quiet \
  --random-order-bucket=global \
    "${TIDS}"
set -e

coverage json > /dev/null
percent=$(cat "${XY_APP_DIR}/coverage.json" | jq .totals.percent_covered)
printf "%.2f\n" "${percent}"

# See https://coverage.readthedocs.io for coverage docs
coverage html \
  --directory "${MY_DIR}/coverage" \
  --precision=2 \
  --quiet
