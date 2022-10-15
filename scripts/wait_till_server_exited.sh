#!/usr/bin/env bash
set -Eeu

# Wait for container to exit. Coverage gathering is done
# in the containers exit handler. Without this wait loop
# we get inconsistent coverage reporting.
SUCCEEDED=0
for x in $(seq 5); do
    if docker ps --filter status=exited | grep -q "${XY_CONTAINER}" ; then
        SUCCEEDED=1
        break
    fi
    echo "Waiting for ${XY_CONTAINER} container to exit"
    sleep 1
done

if [ $SUCCEEDED -eq 0 ]; then
    echo "Failed to stop container ${XY_CONTAINER}"
    exit 1
fi
