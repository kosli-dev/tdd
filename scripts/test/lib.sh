#!/usr/bin/env bash
set -Eeu

export_env_vars() {
  local -r kind="${1}"
  case "${kind}" in
    demo) local -r port=80   ;;
    unit) local -r port=3001 ;;
  system) local -r port=3002 ;;
  esac
  export $(echo_env_vars "${port}" "${kind}")
}

echo_env_vars() {
  local -r port="${1}"
  local -r kind="${2}"  # demo | system | unit
  local -r host_dir="$(git rev-parse --show-toplevel)"
  echo XY_KIND="${kind}"
  echo XY_HOST_PORT="${port}"
  echo XY_HOST_ROOT_DIR="${host_dir}"
  echo XY_HOST_COV_DIR="${host_dir}/coverage/${kind}"
  echo XY_CONTAINER_PORT=8001
  echo XY_CONTAINER_NAME="xy_${kind}"
  echo XY_CONTAINER_ROOT_DIR=/xy
  echo XY_CONTAINER_COV_DIR="/tmp/coverage/${kind}"
  echo XY_IMAGE_NAME=xy_image
  echo XY_NETWORK_NAME=xy_net # Also in docker-compose.yaml
  echo XY_USER_NAME=xy
  echo XY_WORKER_COUNT=2
  echo XY_GIT_COMMIT_SHA="$(git rev-parse HEAD)"
}

ip_address() {
  echo "http://localhost:${XY_HOST_PORT}"
}

die() {
  echo >&2
  echo "Error: $*" >&2
  echo >&2
  exit 43
}

refresh_static_assets() {
  docker run --rm \
    --volume "${XY_HOST_ROOT_DIR}/package.json:/app/package.json:ro" \
    --volume "${XY_HOST_ROOT_DIR}/source/static/scss:/app/scss:rw" \
    --volume "${XY_HOST_ROOT_DIR}/source/static/js:/app/js:rw" \
    --env XY_GIT_COMMIT_SHA \
    ghcr.io/kosli-dev/assets-builder:v1 \
    bash -c "npm run build" \
      || die "refresh_assets.sh failed. Your docker image might be outdated. " \
             "Run 'docker image rm ghcr.io/kosli-dev/assets-builder' and then try again"
}

build_image() {
  cd "${XY_HOST_ROOT_DIR}"
  docker build \
    --build-arg XY_CONTAINER_ROOT_DIR \
    --build-arg XY_CONTAINER_PORT \
    --build-arg XY_USER_NAME \
    --build-arg XY_WORKER_COUNT \
    --build-arg XY_GIT_COMMIT_SHA \
    --file Dockerfile \
    --tag "${XY_IMAGE_NAME}" \
    .
}

bring_network_up() {
  docker network inspect "${XY_NETWORK_NAME}" >/dev/null \
    || docker network create --driver bridge "${XY_NETWORK_NAME}"
}

bring_server_up() {
  # The -p option is to silence warnings about orphan containers.
  sed "s/{NAME}/${XY_KIND}/" "${XY_HOST_ROOT_DIR}/docker-compose.yaml" \
    | docker-compose \
      --env-file="${XY_HOST_ROOT_DIR}/env_vars/test_${XY_KIND}_up.env" \
      --file - \
      -p "${XY_KIND}" \
      up --no-build --detach
}

restart_server() {
  # There are several processes with the name gunicorn.
  # One for the 'master' and one each for the workers.
  # Send SIGHUP to the master which is the oldest (-o).
  docker exec \
    --interactive \
    "${XY_CONTAINER_NAME}" \
    sh -c "pkill -SIGHUP -o gunicorn"
}

wait_till_server_ready() {
  local -r max_tries=15
  local -r url="$(ip_address)/api/health/ready"
  echo -n "Waiting for $(ip_address) readiness"
  for try in $(seq 1 ${max_tries}); do
    echo -n .
    if [ $(curl --silent --write-out '%{http_code}' --output /dev/null "${url}") -eq 200 ]; then
      echo
      return 0
    else
      sleep 0.2
    fi
  done
  echo "Failed $(ip_address) readiness"
  docker container logs "${XY_CONTAINER_NAME}" || true
  exit 42
}

run_tests() {
  case "${XY_KIND}" in
  system) run_tests_system ;;
    unit) run_tests_unit   ;;
  esac
}

run_tests_system() {
  set +e
  docker run \
    --entrypoint="" \
    --env TIDS="${TIDS}" \
    --interactive \
    --net "${XY_NETWORK_NAME}" \
    --rm \
    --volume="${XY_HOST_ROOT_DIR}/test:${XY_CONTAINER_ROOT_DIR}/test:ro" \
    "${XY_IMAGE_NAME}" \
    "${XY_CONTAINER_ROOT_DIR}/test/system/run.sh"
  set -e
}

run_tests_unit() {
  docker exec \
    --env TIDS="${TIDS}" \
    --interactive \
    "${XY_CONTAINER_NAME}" \
    "${XY_CONTAINER_ROOT_DIR}/test/unit/run.sh"
}

gather_coverage() {
  docker exec \
    --env XY_WORKER_COUNT \
    --interactive \
    "${XY_CONTAINER_NAME}" \
    "${XY_CONTAINER_ROOT_DIR}/test/system/gather_coverage.sh" \
    "${XY_CONTAINER_COV_DIR}"
}

get_coverage() {
  rm -rf "${XY_HOST_COV_DIR}" >/dev/null || true
  mkdir -p "${XY_HOST_COV_DIR}"

  docker exec "${XY_CONTAINER_NAME}" tar -cf - -C \
    $(dirname "${XY_CONTAINER_COV_DIR}") $(basename "${XY_CONTAINER_COV_DIR}") \
      | tar -xf - -C "${XY_HOST_COV_DIR}/.."
}

export -f ip_address
export -f wait_till_server_ready
export -f server_restart
export -f run_tests
export -f gather_coverage
export -f tar_pipe_coverage_out
