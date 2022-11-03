#!/usr/bin/env bash
set -Eeu

readonly MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
readonly ROOT_DIR=${MY_DIR}/..

die()
{
    echo  >&2
    echo "Error: $*" >&2
    echo  >&2
    exit 1
}

docker run --rm \
   --volume "${ROOT_DIR}/package.json:/app/package.json" \
   --volume "${ROOT_DIR}/server/static/scss:/app/scss" \
   --volume "${ROOT_DIR}/server/static/js:/app/js" \
   --workdir /app \
   --env COMMIT_SHA=$(git rev-parse HEAD) \
   ghcr.io/kosli-dev/assets-builder:v1 \
   bash -c "npm run build" || \
   die "refresh_assets.sh failed. Your docker image might be outdated. " \
       "Run 'docker image rm ghcr.io/kosli-dev/assets-builder' and then try again"

