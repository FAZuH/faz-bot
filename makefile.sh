#!/bin/bash

SERVICE=$1
ACTION=$2
DOCKER_COMPOSE="./docker/docker-compose.yml"

case $ACTION in
  build)
    docker-compose --file "$DOCKER_COMPOSE" up "$SERVICE" --detach --build 
    ;;
  up)
    docker-compose --file "$DOCKER_COMPOSE" up "$SERVICE" --detach
    ;;
  down)
    docker-compose --file "$DOCKER_COMPOSE" down "$SERVICE"
    ;;
  bash)
    docker exec -it "$SERVICE" /bin/bash
    ;;
  "")
    docker attach "$SERVICE" --no-stdin 
    ;;
  *)
    echo "Invalid action: $ACTION"
    echo "Usage: $0 <service> [build|up|down|bash]"
    exit 1
    ;;
esac
