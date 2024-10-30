#!/bin/bash

SCRIPTS_PATH="scripts"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

UPDATE_SCRIPT="$PROJECT_PATH/scripts/update.sh"

$UPDATE_SCRIPT
