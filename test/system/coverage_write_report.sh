#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# TODO:
# Get coverage to write its pending coverage data to .coverage files
# without shutting down the server. Until then we have to kill the
# server, wail for the server to exit, and then run this script.

coverage combine "${XY_DIR}"

coverage html \
  --directory "${MY_DIR}/coverage" \
  --precision=2 \
  --skip-empty
