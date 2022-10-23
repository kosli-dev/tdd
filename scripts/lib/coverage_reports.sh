#!/usr/bin/env bash
set -Eeu

cov_file_count()
{
  # Find is less noisy than ls when there are no matches
  find . -maxdepth 1 -type f -name '.coverage*' | wc -l | xargs
}

save_coverage_curl()
{
  # Execing into the container to save coverage files doesn't work
  # so it has to be an API route.
  curl \
    --request POST \
    --silent \
    http://localhost:80/api/coverage/save \
    >/dev/null
}

save_coverage()
{
  # Repeat until we have curled each worker process.
  while [ "$(cov_file_count)" != "${XY_WORKERS}" ]
  do
    save_coverage_curl
  done
}

report_coverage()
{
  docker exec \
    --interactive \
    --tty \
    "${XY_CONTAINER}" \
      "${XY_APP_DIR}/test/system/report_coverage.sh"
}

save_coverage
report_coverage

FILE="${XY_REPO_DIR}/test/system/coverage/index.html"
if [ -f "${FILE}" ]; then
  echo "${FILE}"
else
  echo "!!! MISSING...${FILE}"
fi
