#!/usr/bin/env bash
set -Eeu

exec gunicorn \
  --bind "0.0.0.0:${XY_PORT}" \
  --log-level info \
  --threads=4 \
  --workers="${XY_WORKERS}" \
  'xy:app()'
