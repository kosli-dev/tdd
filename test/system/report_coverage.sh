#!/bin/bash -Eu

cd "${XY_APP_DIR}"

status=42
while [ ${status} != 0 ];
do
  # Empirically, we have to loop until this works
  coverage combine --quiet "${XY_APP_DIR}" &> /dev/null
  status=$?
done

set -e
coverage html \
  --directory "${XY_APP_DIR}/test/system/coverage" \
  --precision=2 \
  --quiet
