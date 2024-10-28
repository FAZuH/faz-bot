#!/bin/bash

SERVICE=$1
ACTION=$2
PROJECT_PATH=$(dirname "$(dirname "$(realpath "$0")")")
COMPOSE_FILE="$PROJECT_PATH/docker-compose.yml"

case $ACTION in
  pull)
    docker-compose --file "$COMPOSE_FILE" pull "$SERVICE" --detach
    ;;
  build)
    docker-compose --file "$COMPOSE_FILE" up "$SERVICE" --detach --build 
    ;;
  up)
    docker-compose --file "$COMPOSE_FILE" up "$SERVICE" --detach
    ;;
  down)
    docker-compose --file "$COMPOSE_FILE" down "$SERVICE"
    ;;
  bash)
    docker exec -it "$SERVICE" /bin/bash
    ;;
  "")
    docker attach "$SERVICE" --no-stdin 
    ;;
  *)
    echo "Invalid action: $ACTION"
    echo "Usage: $0 <service> [pull|build|up|down|bash]"
    exit 1
    ;;
esac
