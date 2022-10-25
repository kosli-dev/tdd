#!/usr/bin/env bash
set -Eeu

echo_env_vars() {
  echo XY_REPO_DIR="$(xy_repo_dir)"  # Outside the container
  echo XY_APP_DIR=/xy  # Inside the container
  echo XY_CONTAINER=xy
  echo XY_IMAGE=xy_image
  echo XY_NETWORK=xy_net  # Also in docker-compose.yaml
  echo XY_PORT=8001
  echo XY_USER=xy
  echo XY_WORKERS=2
}

xy_repo_dir() {
  # BASH_SOURCE is empty inside a 'sourced' script
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
  docker network inspect "${XY_NETWORK}" > /dev/null \
    || docker network create --driver bridge "${XY_NETWORK}"
}

server_up() {
  cd "${XY_REPO_DIR}"
  docker-compose \
    --env-file=env_vars/test_system_up.env \
    --file docker-compose.yaml \
      up --no-build --detach
}

wait_till_server_ready() {
  local -r ip_address=localhost
  local -r max_tries=15
  for try in $(seq 1 ${max_tries}); do
    if [ $(curl -sw '%{http_code}' "${ip_address}/ready" -o /dev/null) -eq 200 ]; then
      echo "${ip_address} is ready"
      return 0
    else
      echo "Waiting for ${ip_address} readiness... ${try}/${max_tries}"
      sleep 0.2
    fi
  done
  echo "Failed ${ip_address} readiness"
  docker container logs "${XY_CONTAINER}" || true
  exit 1
}
export -f wait_till_server_ready

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
export -f server_restart

rm_coverage() {
  # Important to _not_ quote the rm'd expression here so * expands
  rm ${XY_REPO_DIR}/.coverage* > /dev/null || true
  rm -rf "${XY_REPO_DIR}/test/system/coverage" > /dev/null || true
}
export -f rm_coverage

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
export -f run_tests
