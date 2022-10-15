#!/usr/bin/env bash
set -Eeu

gunicorn \
  --bind "0.0.0.0:${XY_PORT}" \
  --log-level info \
  --threads=4 \
  --workers=2 \
  'xy:app()'
