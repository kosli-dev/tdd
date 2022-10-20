#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "${MY_DIR}/../.." && pwd)"

# Attempt to run coverage's SIGINT exit-handler (to
# forces coverage to write its pending coverage data
# to .coverage.* file) without actually sending SIGINT
# The idea is that we can re-run system tests without
# having to restart a server (and mongo) and then wait
# for them to be ready.

#OUTPUT_FILE=$(mktemp)
#URL=http://localhost:80/api/company/coverage_write_data
#
#set +e
#HTTP_CODE=$(curl --header 'Content-Type: application/json' \
#  --request POST \
#  --output "${OUTPUT_FILE}" \
#  --write-out "%{http_code}" \
#  "${URL}"
#)
#set -e
#>&2 cat "${OUTPUT_FILE}"
#echo -n .
#echo ${HTTP_CODE}

#docker exec \
#  --interactive \
#  --tty \
#  "${XY_CONTAINER}" \
#    "/${XY_DIR}/test/system/coverage_write_data.py"

# Sending SIGINT does indeed run the coverage exit-handlers
# but it also kills the container...
# Sending SIGHUP restarts the server but does not seem to run
# the coverage exit-handlers, so we get no coverage files.
docker exec \
  --interactive \
  --tty \
  "${XY_CONTAINER}" \
    sh -c "pkill -SIGHUP gunicorn"

# which means the following docker exec to restart
# gunicorn will not work

#docker exec \
#  --interactive \
#  --tty \
#  "${XY_CONTAINER}" \
#    "/${XY_DIR}/server/gunicorn.sh"

#docker run \
#  --entrypoint="" \
#  --interactive \
#  --net "${XY_NETWORK}" \
#  --rm \
#  --tty \
#  --volume="${ROOT_DIR}:/${XY_DIR}" \
#  "${XY_IMAGE}" \
#    "/${XY_DIR}/test/system/coverage_write_data.py"
