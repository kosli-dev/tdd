#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

exec gunicorn \
  --access-logfile - \
  --access-logformat '%(h)s %(l)s %(t)s %(M)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
  --bind="0.0.0.0:${XY_PORT}" \
  --config="${MY_DIR}/gunicorn_config.py" \
  --log-level=info \
  --threads=4 \
  --workers="${XY_WORKERS}" \
  "xy:app()"


