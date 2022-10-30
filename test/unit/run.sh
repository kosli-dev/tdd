#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# See https://coverage.readthedocs.io for coverage docs
# To set the random-ordering seed
#       --random-order-seed=<seed>
set +e
pytest \
  --cache-clear `# Clear .coverage cache. It persists as it is in the volume-mount` \
  --capture=no `# Turn off capturing. Makes print() effects visible and interleaved` \
  --color=yes \
  --cov="${XY_APP_DIR}/" \
  --cov-config="${MY_DIR}/.coveragerc" \
  --cov-report= `# Turn off verbose coverage report` \
  --pythonwarnings=error \
  --quiet \
  --random-order-bucket=global \
    "${TIDS}"
set -e

percent=$(coverage json --quiet -o /dev/stdout | jq .totals.percent_covered)
printf "%.2f%%\n" "${percent}"

coverage html \
  --directory "${MY_DIR}/coverage" \
  --precision=2 \
  --quiet
