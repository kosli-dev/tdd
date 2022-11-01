#!/usr/bin/env bash
set -Eeu

MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

exec gunicorn \
  --bind="0.0.0.0:${XY_PORT}" \
  --config="${MY_DIR}/gunicorn_config.py" \
  --log-level=info \
  --threads=4 \
  --workers=2 \
  "xy:app()"


