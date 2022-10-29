#!/bin/bash -Eu

cd "${XY_APP_DIR}"

ls -al "${XY_APP_DIR}/.coverage*"
#coverage combine "${XY_APP_DIR}"

status=42
while [ ${status} != 0 ];
do
  # We often get the following error
  #   Couldn't use data file '/xy/.coverage': unable to open database file
  # Empirically, if we keep trying it becomes ready.
  coverage combine "${XY_APP_DIR}" # &> /dev/null
  status=$?
done

coverage json > /dev/null
percent=$(cat "${XY_APP_DIR}/coverage.json" | jq .totals.percent_covered)
printf "%.2f\n" "${percent}"

coverage html \
  --directory "${XY_APP_DIR}/test/system/coverage" \
  --precision=2 \
  --quiet
