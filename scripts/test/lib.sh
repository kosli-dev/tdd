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
  echo XY_CONTAINER_PORT=8001
  echo XY_REPO_DIR="$(xy_repo_dir)" # Outside the container
  echo XY_APP_DIR=/xy               # Inside the container
  echo XY_CONTAINER_NAME="xy_${2}"
  echo XY_IMAGE_NAME=xy_image
  echo XY_NETWORK=xy_net # Also in docker-compose.yaml
  echo XY_USER=xy
  echo XY_WORKERS=2
  echo GIT_COMMIT_SHA="$(git rev-parse HEAD)"
}

ip_address() {
  echo "http://localhost:${XY_HOST_PORT}"
}

xy_repo_dir() {
  # Can't use BASH_SOURCE as it's empty inside a 'sourced' script
  git rev-parse --show-toplevel
}

die() {
  echo >&2
  echo "Error: $*" >&2
  echo >&2
  exit 1
}

refresh_assets() {
  docker run --rm \
    --volume "$(xy_repo_dir)/package.json:/app/package.json" \
    --volume "$(xy_repo_dir)/server/static/scss:/app/scss" \
    --volume "$(xy_repo_dir)/server/static/js:/app/js" \
    --workdir /app \
    --env GIT_COMMIT_SHA="${GIT_COMMIT_SHA}" \
    ghcr.io/kosli-dev/assets-builder:v1 \
    bash -c "npm run build" ||
    die "refresh_assets.sh failed. Your docker image might be outdated. " \
      "Run 'docker image rm ghcr.io/kosli-dev/assets-builder' and then try again"
}

build_image() {
  cd "${XY_REPO_DIR}"
  docker build \
    --build-arg XY_APP_DIR \
    --build-arg XY_CONTAINER_PORT \
    --build-arg XY_USER \
    --build-arg XY_WORKERS \
    --build-arg GIT_COMMIT_SHA \
    --file Dockerfile \
    --tag "${XY_IMAGE_NAME}" \
    .
}

network_up() {
  docker network inspect "${XY_NETWORK}" >/dev/null ||
    docker network create --driver bridge "${XY_NETWORK}"
}

server_up() {
  local -r kind="${1}"
  cat "${XY_REPO_DIR}/docker-compose.yaml" | sed "s/{NAME}/${kind}/" \
    | docker-compose \
      --env-file=env_vars/test_system_up.env \
      --file - \
      up --no-build --detach
}

server_restart() {
  # There are several processes with the name gunicorn.
  # One for the 'master' and one each for the workers.
  # Send SIGHUP to the master which is the oldest (-o).
  docker exec \
    --interactive \
    --tty \
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
  exit 1
}

cov_dir() {
  local -r kind="${1}"  # system | unit
  echo "${XY_REPO_DIR}/coverage/${kind}"
}

rm_coverage() {
  rm -rf "$(cov_dir "${1}")" > /dev/null || true
  mkdir -p "$(cov_dir "${1}")"
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
    --volume="${XY_REPO_DIR}/test:${XY_APP_DIR}/test:ro" \
    "${XY_IMAGE_NAME}" \
      "${XY_APP_DIR}/test/system/run.sh"
  set -e
}

report_coverage() {
  docker run \
    --entrypoint="" \
    --env XY_WORKERS \
    --interactive \
    --net "${XY_NETWORK}" \
    --rm \
    --tty \
    --volume="${XY_REPO_DIR}:${XY_APP_DIR}" \
    "${XY_IMAGE_NAME}" \
      "${XY_APP_DIR}/test/system/report_coverage.sh"
}

export -f ip_address
export -f wait_till_server_ready
export -f server_restart
export -f rm_coverage
export -f cov_dir
export -f run_tests
export -f report_coverage
