#!/bin/bash

set -e

DOCKER_COMPOSE_FILE="/home/faz/Workspace/Development/faz-bot/docker/docker-compose.yml"
DOCKER_COMPOSE_CMD="docker-compose -f $DOCKER_COMPOSE_FILE"

echo "Pulling latest images..."
$DOCKER_COMPOSE_CMD pull

echo "Stopping and removing existing containers..."
$DOCKER_COMPOSE_CMD down

echo "Starting new containers..."
$DOCKER_COMPOSE_CMD up -d

echo "Removing old images..."
docker image prune -f

echo "Deployment completed successfully."
