#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
source "${MY_DIR}/lib.sh"
export_env_vars demo

combine_test_coverage()
{
  docker run \
    --tty \
    --rm \
    --volume "${XY_HOST_ROOT_DIR}/test:${XY_CONTAINER_ROOT_DIR}/test:ro" \
    --volume "${XY_HOST_ROOT_DIR}/source:${XY_CONTAINER_ROOT_DIR}/source:ro" \
    --volume "${XY_HOST_ROOT_DIR}/coverage/all:${XY_CONTAINER_ROOT_DIR}/coverage/all:rw" \
    "${XY_IMAGE_NAME}" \
    ${XY_CONTAINER_ROOT_DIR}/test/all/combine_coverage.sh \
      ${XY_CONTAINER_ROOT_DIR}/coverage/all

  echo ${XY_HOST_ROOT_DIR}/coverage/all/index.html
}

combine_test_coverage
