#!/usr/bin/env bash
set -Eeu

curl \
  --request POST \
  --silent \
  http://localhost:80/api/company/coverage_report \
    > /dev/null

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "${MY_DIR}/../.." && pwd)"
echo "${ROOT_DIR}/test/system/coverage/index.html"
