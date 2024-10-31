#!/bin/bash

SCRIPTS_PATH="scripts"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

UPDATE_SCRIPT="$PROJECT_PATH/scripts/update.sh"

set -e


main() {
    $COMPOSE up mysql -d

    $UPDATE_SCRIPT

    echo "Pulling latest images..."
    $COMPOSE pull 

    echo "Stopping and removing existing containers..."
    $COMPOSE down

    echo "Starting new containers..."
    $COMPOSE up -d

    echo "Removing old images..."
    docker image prune -f

    echo "Update completed successfully."
}

main
