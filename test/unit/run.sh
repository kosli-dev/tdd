#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly COV_DIR="${1}"

run_tests()
{
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

create_coverage()
{
  pushd "${COV_DIR}" > /dev/null
  coverage combine --keep --quiet
  create_coverage_json
  create_coverage_html
  popd > /dev/null
}

create_coverage_json()
{
  local -r filename="${COV_DIR}/coverage.json"

  coverage json \
    -o "${filename}" \
    --pretty-print \
    --quiet

  printf "%.2f%%\n" "$(jq .totals.percent_covered "${filename}")"
}

create_coverage_html()
{
  coverage html \
    --data-file=.coverage.unit \
    --directory="${COV_DIR}" \
    --precision=2 \
    --quiet
}

run_tests
create_coverage
