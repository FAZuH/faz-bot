#!/bin/bash

SCRIPTS_PATH="scripts"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

SERVICE=$1
ACTION=$2

case $ACTION in
    pull)
        $COMPOSE pull "$SERVICE"
        ;;
    build)
        $COMPOSE up "$SERVICE" --detach --build 
        ;;
    up)
        $COMPOSE up "$SERVICE" --detach
        ;;
    down)
        $COMPOSE down "$SERVICE"
        ;;
    bash)
        $COMPOSE exec -it "$SERVICE" /bin/bash
        ;;
    "")
        $COMPOSE attach "$SERVICE" --no-stdin 
        ;;
    *)
        echo "Invalid action: $ACTION"
        echo "Usage: $0 <service> [pull|build|up|down|bash]"
        exit 1
        ;;
esac
