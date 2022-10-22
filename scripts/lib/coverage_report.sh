#!/usr/bin/env bash
set -Eeu

readonly URL=http://localhost:80/api/company/coverage_report

curl --header 'Content-Type: application/json' \
  --request POST \
  --silent \
  --write-out "%{http_code}" \
  "${URL}" > /dev/null

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "${MY_DIR}/../.." && pwd)"
echo "${ROOT_DIR}/test/system/coverage/index.html"
