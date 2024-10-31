#!/bin/bash

SCRIPTS_PATH="scripts"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

UPDATE_SCRIPT="$PROJECT_PATH/scripts/update.sh"

set -e


main() {
    $UPDATE_SCRIPT

    echo "Pulling latest images..."
    $COMPOSE pull 

    echo "Stopping and removing existing containers..."
    $COMPOSE down

    echo "Starting new containers..."
    $COMPOSE up -d

    echo "Removing old images..."
    $COMPOSE image prune -f

    echo "Update completed successfully."
}

main
