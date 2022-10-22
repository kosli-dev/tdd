#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "${MY_DIR}/../.." && pwd)"

rm ${ROOT_DIR}/.coverage* || true
rm -rf ${ROOT_DIR}/test/system/coverage || true
