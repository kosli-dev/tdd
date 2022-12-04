#!/bin/bash -Eu

cov_dir() {
  echo "/tmp/coverage/system"
}

actual_coverage_files_count() {
  # Find is less noisy than ls when there are no matches
  find "$(cov_dir)" -maxdepth 1 -type f -name '.coverage*' | wc -l | xargs
}

wait_for_all_coverage_files_based_on_workers_count() {
  # We have sent a SIGHUP to the gunicorn master which will restart
  # each worker. Now we wait for each workers' sigterm handler to
  # write its .coverage file.
  local -r max_tries=20
  for i in $(seq "${max_tries}"); do
    echo -n .
    [ "$(actual_coverage_files_count)" == "${XY_WORKER_COUNT}" ] && break
    sleep 0.1
  done
  echo .
  if [ "${i}" == "${max_tries}" ]; then
    echo "Gave up waiting for all .coverage files after "${max_tries}" tries"
  fi
}

wait_for_all_coverage_files_based_on_stabilizing() {
  # Occasionally you might want to wait until the number of
  # .coverage files stabilizes. Eg you are working without
  # a network connection and cannot do a `docker build`.
  while : ; do
    echo -n .
    a1="$(actual_coverage_files_count)"; sleep 0.1
    a2="$(actual_coverage_files_count)"; sleep 0.1
    a3="$(actual_coverage_files_count)"; sleep 0.1
    [ "${a1}${a2}${a3}" == "${a1}${a2}${a3}" ] && break
  done
  echo .
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

wait_for_all_coverage_files_based_on_workers_count
cd "$(cov_dir)"
coverage combine .
create_coverage_json
create_coverage_html