#!/usr/bin/env bash
set -Eeu

exec gunicorn \
  --bind "0.0.0.0:${XY_PORT}" \
  --log-level info \
  'xy:app()'

# TODO: get combined coverage of both workers
#  --threads=4 \
#  --workers=2 \
