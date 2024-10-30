#!/bin/bash

SCRIPTS_PATH="scripts"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

set -e


main() {
    cd "$PROJECT_PATH" || exit

    git pull origin main

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
