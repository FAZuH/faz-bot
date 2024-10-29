#!/bin/bash

SERVICE=$1
ACTION=$2

case $ACTION in
  pull)
    docker-compose pull "$SERVICE"
    ;;
  build)
    docker-compose up "$SERVICE" --detach --build 
    ;;
  up)
    docker-compose up "$SERVICE" --detach
    ;;
  down)
    docker-compose down "$SERVICE"
    ;;
  bash)
    docker-compose exec -it "$SERVICE" /bin/bash
    ;;
  "")
    docker-compose attach "$SERVICE" --no-stdin 
    ;;
  *)
    echo "Invalid action: $ACTION"
    echo "Usage: $0 <service> [pull|build|up|down|bash]"
    exit 1
    ;;
esac
