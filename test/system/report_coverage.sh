#!/bin/bash -Eu

cov_dir() {
  echo "${XY_APP_DIR}/coverage/system"
}

actual_coverage_files_count() {
  # Find is less noisy than ls when there are no matches
  find "$(cov_dir)" -maxdepth 1 -type f -name '.coverage*' | wc -l | xargs
}

wait_for_all_coverage_files() {
  # We have sent a SIGHUP to gunicorn master
  # So now we have to wait for all sigterm handlers
  # to write their .coverage file.
  # We don't know how many .coverage files there will be!
  # So we empirically wait until they "settle"
  while : ; do
    echo -n .
    a1=$(actual_coverage_files_count); sleep 0.2
    a2=$(actual_coverage_files_count); sleep 0.2
    a3=$(actual_coverage_files_count); sleep 0.2
    [ "${a1}${a2}${a3}" == "${a1}${a1}${a1}" ] && break
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
