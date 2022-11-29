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
    --ignore="${XY_APP_DIR}/test/system" \
    -o cache_dir=/tmp \
    --pythonwarnings=error \
    --quiet \
    --random-order-bucket=global \
      "${TIDS}"
  set -e
}

coverage_percent() {
  local -r tmp_file=/tmp/coverage.unit.json
  coverage json --quiet -o "${tmp_file}"
  jq .totals.percent_covered "${tmp_file}"
}

coverage_report() {
  coverage html \
    --directory "$(cov_dir)" \
    --precision=2 \
    --quiet
}

run_tests
cd $(cov_dir)
# coverage combine .
printf "%.2f%%\n" "$(coverage_percent)"
coverage_report
