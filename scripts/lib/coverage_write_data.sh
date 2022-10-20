#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

OUTPUT_FILE=$(mktemp)
URL=http://localhost:80/api/company/coverage_write_data

set +e
HTTP_CODE=$(curl --header 'Content-Type: application/json' \
  --request POST \
  --output "${OUTPUT_FILE}" \
  --write-out "%{http_code}" \
  "${URL}"
)
set -e
>&2 cat "${OUTPUT_FILE}"
echo -n .
echo "${HTTP_CODE}"
