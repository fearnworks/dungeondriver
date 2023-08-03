#!/bin/bash
set -o allexport
source ./.env
set +o allexport

cd ./dungeon_driver

IMAGE_NAME="ghcr.io/fearnworks/dungeon_driver"
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
GIT_COMMIT=$(git rev-parse --short HEAD)

# Authenticate with the GitHub Container Registry
echo "$REG_TOKEN" | docker login ghcr.io -u USERNAME --password-stdin

docker build -t "$IMAGE_NAME:$GIT_BRANCH" \
-t "$IMAGE_NAME:$GIT_COMMIT" .

docker push "$IMAGE_NAME:$GIT_BRANCH"
docker push "$IMAGE_NAME:$GIT_COMMIT"
