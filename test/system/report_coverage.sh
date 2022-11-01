#!/bin/bash -Eu

cov_dir() {
  echo "${XY_APP_DIR}/coverage/system"
}

actual_coverage_files_count() {
  # Find is less noisy than ls when there are no matches
  find "$(cov_dir)" -maxdepth 1 -type f -name '.coverage*' | wc -l | xargs
}

wait_for_all_coverage_files() {
  # We have sent a SIGHUP to the gunicorn master which will restart
  # each worker. Now we wait for each workers' sigterm handler to
  # write its .coverage file.
  while : ; do
    echo -n .
    [ "$(actual_coverage_files_count)" == "${XY_WORKERS}" ] && break
    sleep 0.1
  done
  echo .
}

coverage_percent() {
  local -r tmp_file=/tmp/coverage.system.json
  coverage json --quiet -o "${tmp_file}"
  jq .totals.percent_covered "${tmp_file}"
}

wait_for_all_coverage_files
cd "$(cov_dir)"
coverage combine .
printf "%.2f%%\n" "$(coverage_percent)"
coverage html \
  --directory "$(cov_dir)" \
  --precision=2 \
  --quiet
