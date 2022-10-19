#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# To set the random-ordering seed
#       --random-order-seed=<seed>

pytest \
  --cache-clear `# Clear .coverage cache. It persists as it is in the volume-mount` \
  --capture=no `# Turn off capturing. Makes print() effects visible and interleaved` \
  --color=yes \
  --cov="/${XY_DIR}/server/" \
  --cov-config="${MY_DIR}/.coveragerc" \
  --cov-report= `# Turn off verbose coverage report` \
  --ignore=test/system \
  --pythonwarnings=error \
  --quiet \
  --random-order-bucket=global \
    "${TIDS}"

# See https://coverage.readthedocs.io for coverage docs
coverage html \
  --directory "${MY_DIR}/coverage" \
  --precision=2 \
  --skip-empty > /dev/null
