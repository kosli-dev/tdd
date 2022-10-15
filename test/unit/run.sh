#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#readonly BASE_DIR="$(cd "${MY_DIR}/../.." && pwd)/tmp/test/unit"
#rm -rf "${BASE_DIR}" || true
#mkdir -p "${BASE_DIR}" || true

run_tests()
{
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
}

gather_coverage()
{
  # See https://coverage.readthedocs.io for coverage docs
  coverage report --skip-empty --show-missing --precision=2
  coverage html --precision=2 --directory "${MY_DIR}/coverage"
}

run_tests "$@"
gather_coverage
