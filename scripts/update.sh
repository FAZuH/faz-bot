#!/bin/bash

set -e

echo "Pulling latest images..."
docker-compose pull

echo "Stopping and removing existing containers..."
docker-compose down

echo "Starting new containers..."
docker-compose up -d

echo "Removing old images..."
docker image prune -f

echo "Update completed successfully."
