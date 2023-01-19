#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

if [ -z "${COVERAGE_PROCESS_START:-}" ]; then
  COVERAGE_CONFIG=
else
  COVERAGE_CONFIG="--config ${MY_DIR}/gunicorn_coverage.py"
fi

mkdir /tmp/strangler_logs

gunicorn \
  --access-logfile - \
  --access-logformat '%(h)s %(l)s %(t)s %(M)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
  --bind="0.0.0.0:${XY_CONTAINER_PORT}" \
  ${COVERAGE_CONFIG} \
  --log-level=info \
  --threads=4 \
  --workers=2 \
  "xy:app()"
