#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
readonly COV_DIR="${1}"

combine_coverage()
{
  local -r rcfile="${MY_DIR}/.coveragerc"
  pushd "${COV_DIR}" >/dev/null
  coverage combine --keep --quiet --rcfile="${rcfile}"
  coverage json --pretty-print --quiet -o "${COV_DIR}/coverage.json" --rcfile="${rcfile}"
  coverage html --quiet --skip-covered --precision=2 --directory="${COV_DIR}" --rcfile="${rcfile}"
  popd >/dev/null
}

combine_coverage
