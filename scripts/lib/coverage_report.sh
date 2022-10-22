#!/usr/bin/env bash
set -Eeu

curl \
  --request POST \
  --silent \
  http://localhost:80/api/coverage/report \
    > /dev/null

FILE="${XY_REPO_DIR}/test/system/coverage/index.html"
if [ -f "${FILE}" ]; then
  echo "${FILE}"
else
  echo "!!! MISSING...${FILE}"
fi
