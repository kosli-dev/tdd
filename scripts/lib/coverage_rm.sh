#!/usr/bin/env bash
set -Eeu

# Important to _not_ quote the rm'd expression here so * expands
rm ${XY_REPO_DIR}/.coverage* > /dev/null || true
rm -rf "${XY_REPO_DIR}/test/unit/coverage"   > /dev/null || true
rm -rf "${XY_REPO_DIR}/test/system/coverage" > /dev/null || true
