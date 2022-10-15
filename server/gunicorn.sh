#!/usr/bin/env bash
set -Eeu

# exec replaces current process with the gunicorn instead of starting it as
# a separate process. This makes gunicorn the process with PID=1
# We need gunicorn to run with PID=1 so that the SIGINT signal sent when stopping
# the system tests is sent to gunicorn and it stops gracefully.

exec gunicorn \
  --bind 0.0.0.0:${XY_PORT} \
  --threads=4 \
  --workers=2 \
  'xy:app()'
