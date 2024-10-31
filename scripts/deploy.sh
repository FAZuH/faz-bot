#!/bin/bash

SCRIPTS_PATH="scripts"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

UPDATE_SCRIPT="$PROJECT_PATH/scripts/update.sh"

set -e


main() {
    # 1. Make sure database is running
    $COMPOSE up mysql -d
    "docker/wait-for-it.sh" -t 5 mysql:3306 -- echo "MySQL is ready!"

    # 2. Pull git changes and update database
    $UPDATE_SCRIPT

    echo "Pulling latest images..."
    # 3. Pull latest docker images
    $COMPOSE pull 

    echo "Starting new containers..."
    # 4. Start fazcollect and fazcord service
    $COMPOSE up fazcollect fazcord -d

    echo "Removing old images..."
    # 5. Remove old images
    docker image prune -f

    echo "Update completed successfully."
}

main
