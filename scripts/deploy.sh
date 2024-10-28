#!/bin/bash

SCRIPTS_PATH="$(dirname "$(realpath "$0")")"
PROJECT_PATH=$(dirname "$(dirname "$(realpath "$0")")")
cd "$PROJECT_PATH" || exit

echo "Pulling latest git commit in $PROJECT_PATH..."
git pull origin main

echo "Running update script..."
UPDATE_SCRIPT="$PROJECT_PATH/scripts/update.sh"

$UPDATE_SCRIPT
