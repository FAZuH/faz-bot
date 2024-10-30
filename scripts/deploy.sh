#!/bin/bash

SCRIPTS_PATH="$(dirname "$(realpath "$0")")"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

UPDATE_SCRIPT="$PROJECT_PATH/scripts/update.sh"

$UPDATE_SCRIPT
