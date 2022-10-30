#!/bin/bash -Eu

cd "${XY_APP_DIR}"

coverage_file_count() {
  # Find is less noisy than ls when there are no matches
  find "${XY_APP_DIR}" -maxdepth 1 -type f -name '.coverage*' | wc -l | xargs
}

wait_for_all_coverage_files() {
  # We have sent a SIGHUP to gunicorn master
  # So now we have to wait for all sigterm handlers
  # to write their coverage file
  while [ "$(coverage_file_count)" != 4 ]; do
    echo -n .
    sleep 0.1
  done
  echo .
}

wait_for_all_coverage_files

coverage combine "${XY_APP_DIR}" #&> /dev/null

coverage json > /dev/null
percent=$(cat "${XY_APP_DIR}/coverage.json" | jq .totals.percent_covered)
printf "%.2f\n" "${percent}"

coverage html \
  --directory "${XY_APP_DIR}/test/system/coverage" \
  --precision=2 \
  --quiet
