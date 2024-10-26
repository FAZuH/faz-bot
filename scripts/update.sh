#!/bin/bash

set -e

scrDir=$(dirname "$(realpath "$0")")

COMPOSE_FILE="$scrDir/docker-compose.yml"
COMPOSE_CMD="docker-compose --file $COMPOSE_FILE"

echo "Pulling latest images..."
$COMPOSE_CMD pull

echo "Stopping and removing existing containers..."
$COMPOSE_CMD down

echo "Starting new containers..."
$COMPOSE_CMD up -d

echo "Removing old images..."
docker image prune -f

echo "Update completed successfully."
