#!/usr/bin/env bash
set -Eeu

readonly IP_ADDRESS=localhost
readonly MAX_TRIES=3

for try in $(seq 1 ${MAX_TRIES}); do
  if [ $(curl -sw '%{http_code}' "${IP_ADDRESS}/ready" -o /dev/null) -eq 200 ]; then
    echo "${IP_ADDRESS} is ready"
    exit 0
  else
    echo "Waiting for ${IP_ADDRESS} readiness... ${try}/${MAX_TRIES}"
    sleep 1
  fi
done
echo "Failed ${IP_ADDRESS} readiness"
docker container logs "${APP_CONTAINER}" || true
exit 1
