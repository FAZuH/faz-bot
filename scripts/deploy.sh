#!/bin/bash

SCRIPTS_PATH="scripts"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

UPDATE_SCRIPT="$PROJECT_PATH/scripts/update.sh"

set -e


main() {
    # 1. Make sure database is running before updating it. Needed for step 2
    $COMPOSE up mysql -d
    "docker/wait-for-it.sh" -t 5 mysql:3306 -- echo "MySQL is ready!"

    # 2. Pull git changes and update database.
    # This is to ensure scripts and docker configs are 
    # in the latest version before running docker-compose pull
    $UPDATE_SCRIPT

    echo "Pulling latest images..."
    # 3. Pull latest docker images
    $COMPOSE pull 

    echo "Starting new containers..."
    # 4. Start services
    # Note that docker will only recreate containers 
    # if the image (or docker-compose config) has changed
    $COMPOSE up mysql fazcollect fazcord -d

    echo "Removing old images..."
    # 5. Remove old images (if any)
    docker image prune -f

    echo "Update completed successfully."
}

main
