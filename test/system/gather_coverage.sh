#!/bin/bash -Eeu

# Integration tests make HTTP calls to the server which is running in
# a different container to the container running the tests.
# We want coverage stats, but we don't want them for the tests,
# we want them for the code running in the server. To get them we
# need to jump through a few hoops, as detailed in this dir's README.md and
# run.sh files.

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# See https://coverage.readthedocs.io for coverage docs
coverage combine
coverage report --skip-empty --show-missing --precision=2
coverage html --precision=2 --directory "${MY_DIR}/coverage"
