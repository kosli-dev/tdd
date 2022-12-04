#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cov_dir() {
  echo "/tmp/coverage/unit"
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
    --cov="${XY_CONTAINER_ROOT_DIR}/" \
    --cov-config="${MY_DIR}/.coveragerc" \
    --cov-report= `# Turn off verbose coverage report` \
    --ignore="${XY_CONTAINER_ROOT_DIR}/test/system" \
    -o cache_dir=/tmp \
    --pythonwarnings=error \
    --quiet \
    --random-order-bucket=global \
      "${TIDS}"
  set -e
}

create_coverage_json() {
  local -r filename="$(cov_dir)/coverage.json"
  coverage json --pretty-print --quiet -o "${filename}"
  printf "%.2f%%\n" "$(jq .totals.percent_covered "${filename}")"
}

create_coverage_html() {
  coverage html \
    --directory "$(cov_dir)" \
    --precision=2 \
    --quiet
}

run_tests
cd $(cov_dir)
create_coverage_json
create_coverage_html
