#!/usr/bin/env bash
set -Eeu

echo_env_vars() {
  echo XY_REPO_DIR="$(xy_repo_dir)" # Outside the container
  echo XY_APP_DIR=/xy               # Inside the container
  echo XY_CONTAINER=xy
  echo XY_IMAGE=xy_image
  echo XY_NETWORK=xy_net # Also in docker-compose.yaml
  echo XY_PORT=8001
  echo XY_USER=xy
  echo XY_WORKERS=2
}

ip_address() {
  echo "http://localhost:80"
}

xy_repo_dir() {
  # Can't use BASH_SOURCE as it's empty inside a 'sourced' script
  git rev-parse --show-toplevel
}

build_image() {
  cd "${XY_REPO_DIR}"
  docker build \
    --build-arg XY_APP_DIR \
    --build-arg XY_PORT \
    --build-arg XY_USER \
    --build-arg XY_WORKERS \
    --file Dockerfile \
    --tag "${XY_IMAGE}" \
    .
}

network_up() {
  docker network inspect "${XY_NETWORK}" >/dev/null ||
    docker network create --driver bridge "${XY_NETWORK}"
}

server_up() {
  cd "${XY_REPO_DIR}"
  docker-compose \
    --env-file=env_vars/test_system_up.env \
    --file docker-compose.yaml \
    up --no-build --detach
}

wait_till_server_ready() {
  local -r max_tries=15
  local -r url="$(ip_address)/api/health/ready"
  for try in $(seq 1 ${max_tries}); do
    if [ $(curl --silent --write-out '%{http_code}' --output /dev/null "${url}") -eq 200 ]; then
      return 0
    else
      echo "Waiting for $(ip_address) readiness... ${try}/${max_tries}"
      sleep 0.2
    fi
  done
  echo "Failed $(ip_address) readiness"
  docker container logs "${XY_CONTAINER}" || true
  exit 1
}

server_restart() {
  # There are several processes with the name gunicorn.
  # One for the 'master' and one each for the workers.
  # Send SIGHUP to the master which is the oldest (-o).
  docker exec \
    --interactive \
    --tty \
    "${XY_CONTAINER}" \
    sh -c "pkill -SIGHUP -o gunicorn"
}

rm_coverage() {
  # Important to _not_ quote the rm'd expression here so * expands
  rm -f ${XY_REPO_DIR}/.coverage > /dev/null || true
  rm -f ${XY_REPO_DIR}/.coverage.* > /dev/null || true
  rm -rf "${XY_REPO_DIR}/test/system/coverage" > /dev/null || true
}

run_tests() {
  set +e
  docker run \
    --entrypoint="" \
    --env TIDS="${TIDS}" \
    --interactive \
    --net "${XY_NETWORK}" \
    --rm \
    --tty \
    --volume="${XY_REPO_DIR}:${XY_APP_DIR}" \
    "${XY_IMAGE}" \
      "${XY_APP_DIR}/test/system/run.sh"
  set -e
}

report_coverage() {
  docker run \
    --entrypoint="" \
    --interactive \
    --net "${XY_NETWORK}" \
    --rm \
    --tty \
    --volume="${XY_REPO_DIR}:${XY_APP_DIR}" \
    "${XY_IMAGE}" \
      "${XY_APP_DIR}/test/system/report_coverage.sh"
}

export -f ip_address
export -f wait_till_server_ready
export -f server_restart
export -f rm_coverage
export -f run_tests
export -f report_coverage
