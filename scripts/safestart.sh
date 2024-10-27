#!/bin/bash

PYTHON_MODULE=$1
DB_VERSION_RANGES=$2  # Space separated list of database versions ranges
DB_NAMES=$3           # Space separated list of database names
WEBHOOK_VAR_NAMES=$4  # Space separated list of webhook environment variable names
SCRIPTS_PATH="$(dirname "$(realpath "$0")")"


"$SCRIPTS_PATH/checkhealth.sh" "$DB_VERSION_RANGES" "$DB_NAMES" "$WEBHOOK_VAR_NAMES" 

res=$?
if [[ "$res" != 0 ]]; then
    echo "Error: Health check failed. Exiting."
    # To give developers time to connect to the container and debug
    sleep 500
    exit 1
fi

python -m "$PYTHON_MODULE"
