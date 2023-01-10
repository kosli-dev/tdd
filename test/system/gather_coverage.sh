#!/bin/bash -Eu

readonly COV_DIR="${1}"

actual_coverage_files_count()
{
  find "${COV_DIR}" -maxdepth 1 -type f -name ^.coverage | wc -l | xargs
}

wait_for_all_coverage_files()
{
  while : ; do
    echo -n .
    a1="$(actual_coverage_files_count)"; sleep 0.25
    a2="$(actual_coverage_files_count)"; sleep 0.25
    a3="$(actual_coverage_files_count)"; sleep 0.25
    a4="$(actual_coverage_files_count)"; sleep 0.25
    [ "${a1}${a2}${a3}${a4}" == "${a1}${a1}${a1}${a1}" ] && break
  done
  echo .
}

create_coverage_json()
{
  local -r filename="${COV_DIR}/coverage.json"

  coverage json \
    -o "${filename}" `#NB: Not -o=... ` \
    --pretty-print \
    --quiet

  printf "%.2f%%\n" "$(jq .totals.percent_covered "${filename}")"
}

create_coverage_html()
{
  coverage html \
    --directory="${COV_DIR}" \
    --precision=2 \
    --quiet
}

wait_for_all_coverage_files
cd "${COV_DIR}"
coverage combine --keep --quiet
create_coverage_json
create_coverage_html
