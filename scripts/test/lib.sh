#!/usr/bin/env bash
set -Eeu

export_env_vars() {
  local -r kind="${1}"
  case "${kind}" in
    demo) local -r port=80;;
    unit) local -r port=3001;;
    system) local -r port=3002;;
  esac
  export $(echo_env_vars "${port}" "${kind}")
}

echo_env_vars() {
  echo XY_HOST_PORT="${1}"
  echo XY_HOST_DIR="$(git rev-parse --show-toplevel)"
  echo XY_CONTAINER_PORT=8001
  echo XY_CONTAINER_NAME="xy_${2}"
  echo XY_CONTAINER_DIR=/xy
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
  exit 1
}

refresh_assets() {
  docker run --rm \
    --volume "${XY_HOST_DIR}/package.json:/app/package.json" \
    --volume "${XY_HOST_DIR}/server/static/scss:/app/scss" \
    --volume "${XY_HOST_DIR}/server/static/js:/app/js" \
    --workdir /app \
    --env XY_GIT_COMMIT_SHA \
    ghcr.io/kosli-dev/assets-builder:v1 \
    bash -c "npm run build" ||
    die "refresh_assets.sh failed. Your docker image might be outdated. " \
      "Run 'docker image rm ghcr.io/kosli-dev/assets-builder' and then try again"
}

build_image() {
  cd "${XY_HOST_DIR}"
  docker build \
    --build-arg XY_CONTAINER_DIR \
    --build-arg XY_CONTAINER_PORT \
    --build-arg XY_USER_NAME \
    --build-arg XY_WORKER_COUNT \
    --build-arg XY_GIT_COMMIT_SHA \
    --file Dockerfile \
    --tag "${XY_IMAGE_NAME}" \
    .
}

network_up() {
  docker network inspect "${XY_NETWORK_NAME}" >/dev/null ||
    docker network create --driver bridge "${XY_NETWORK_NAME}"
}

server_up() {
  # The -p option is to silence warnings about orphan containers.
  local -r kind="${1}"
  sed "s/{NAME}/${kind}/" "${XY_HOST_DIR}/docker-compose.yaml" \
    | docker-compose \
      --env-file=env_vars/test_system_up.env \
      --file - \
      -p "${kind}" \
      up --no-build --detach
}

server_restart() {
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
  for try in $(seq 1 ${max_tries}); do
    if [ $(curl --silent --write-out '%{http_code}' --output /dev/null "${url}") -eq 200 ]; then
      return 0
    else
      echo "Waiting for $(ip_address) readiness... ${try}/${max_tries}"
      sleep 0.2
    fi
  done
  echo "Failed $(ip_address) readiness"
  docker container logs "${XY_CONTAINER_NAME}" || true
  exit 42
}

host_cov_dir() {
  local -r kind="${1}"  # system | unit
  echo "${XY_HOST_DIR}/coverage/${kind}"
}

rm_coverage() {
  local -r cov_dir="$(host_cov_dir "${1}")"
  rm -rf "${cov_dir}" > /dev/null || true
  mkdir -p "${cov_dir}"
}

run_tests() {
  set +e
  docker run \
    --entrypoint="" \
    --env TIDS="${TIDS}" \
    --interactive \
    --net "${XY_NETWORK_NAME}" \
    --rm \
    --volume="${XY_HOST_DIR}/test:${XY_CONTAINER_DIR}/test:ro" \
    "${XY_IMAGE_NAME}" \
      "${XY_CONTAINER_DIR}/test/system/run.sh"
  set -e
}

report_coverage() {
  docker exec \
    --env XY_WORKER_COUNT \
    --interactive \
    "${XY_CONTAINER_NAME}" \
      "${XY_CONTAINER_DIR}/test/system/report_coverage.sh"
}

tar_pipe_coverage_out() {
  local -r kind="${1}"
  local -r cov_dir="/tmp/coverage/${kind}"
  docker exec "${XY_CONTAINER_NAME}" tar -cf - -C \
    $(dirname "${cov_dir}") $(basename "${cov_dir}") \
    | tar -xf - -C "${XY_HOST_DIR}/coverage"
}

export -f ip_address
export -f wait_till_server_ready
export -f server_restart
export -f rm_coverage
export -f host_cov_dir
export -f run_tests
export -f report_coverage
export -f tar_pipe_coverage_out