#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cov_dir() {
  echo "${XY_APP_DIR}/coverage/unit"
}

run_tests() {
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
}

coverage_percent() {
  coverage json --quiet -o /dev/stdout | jq .totals.percent_covered
}

coverage_report() {
  coverage html \
    --directory "$(cov_dir)" \
    --precision=2 \
    --quiet
}

run_tests
cd $(cov_dir)
printf "%.2f%%\n" "$(coverage_percent)"
coverage_report
