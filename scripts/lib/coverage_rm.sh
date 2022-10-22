#!/usr/bin/env bash
set -Eeu

# Important to _not_ quote the rm'd expression here so * expands
rm ${XY_HOME_DIR}/.coverage* > /dev/null || true
