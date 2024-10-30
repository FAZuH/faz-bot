#!/bin/bash

# --------- #
# Variables #
# --------- #

SCRIPTS_PATH="scripts"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

COMPOSE="docker-compose --file $PROJECT_PATH/docker-compose.yml"

export COMPOSE

# --------- #
# Functions #
# --------- #

loadenv() {
    if [ -f .env ]; then
        export $(cat .env | xargs)
    fi
}

checkenv() {
    required_vars=(
        "MYSQL_ROOT_PASSWORD"
        "MYSQL_HOST"
        "MYSQL_PORT"
        "MYSQL_USER"
        "MYSQL_PASSWORD"
        "MYSQL_FAZWYNN_DATABASE"
        "MYSQL_FAZCORD_DATABASE"
    )

    for var in "${required_vars[@]}"; do
        if [ -z "${!var:-}" ]; then
            echo "Error: Required environment variable $var is not set"
            exit 1
        fi
    done
}
