#!/usr/bin/env bash
set -Eeu

cov_file_count()
{
  #find . -maxdepth 1 -type f -name '.coverage*' | wc -l | xargs
  ls ${XY_REPO_DIR}/.coverage* | wc -l | xargs
}

save_coverage()
{
  curl \
    --request POST \
    --silent \
    http://localhost:80/api/coverage/save \
    >/dev/null
}

report_coverage()
{
  docker exec \
    --interactive \
    --tty \
    "${XY_CONTAINER}" \
      "${XY_APP_DIR}/test/system/report_coverage.sh"
}

while [ "$(cov_file_count)" != '2' ]
do
  save_coverage
done
report_coverage

FILE="${XY_REPO_DIR}/test/system/coverage/index.html"
if [ -f "${FILE}" ]; then
  echo "${FILE}"
else
  echo "!!! MISSING...${FILE}"
fi
