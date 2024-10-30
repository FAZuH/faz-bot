#!/bin/bash

SCRIPTS_PATH="$(dirname "$(realpath "$0")")"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

UPDATE_SCRIPT="$PROJECT_PATH/scripts/update.sh"

$UPDATE_SCRIPT
