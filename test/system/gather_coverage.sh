#!/bin/bash -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

coverage combine
coverage report --skip-empty --show-missing --precision=2
coverage html --precision=2 --directory "${MY_DIR}/coverage"
