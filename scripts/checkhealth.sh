#!/bin/bash

DB_VERSION_RANGES=$1  # Space separated list of database versions ranges
DB_NAMES=$2           # Space separated list of database names
WEBHOOK_VAR_NAMES=$3  # Space separated list of webhook environment variable names

PROJECT_PATH="$(dirname "$(dirname "$(realpath "$0")")")"
SCRIPT_PATH="$PROJECT_PATH/scripts"
VERSION_CHECK_FILE="$SCRIPT_PATH/_version_check.py"

# Convert space-separated strings into arrays
IFS=' ' read -r -a ARR_WEBHOOK <<< "$WEBHOOK_VAR_NAMES"
IFS=' ' read -r -a ARR_VERSION <<< "$DB_VERSION_RANGES"
IFS=' ' read -r -a ARR_DB_NAME <<< "$DB_NAMES"

# Ensure the lengths of the arrays match
if [ ${#ARR_WEBHOOK[@]} -ne ${#ARR_VERSION[@]} ] || [ ${#ARR_VERSION[@]} -ne ${#ARR_DB_NAME[@]} ]; then
    echo "Error: The number of minimum versions, maximum versions, and database names must match."
    exit 1
fi

send_discord_error() {
    local version="$1"
    local ver_range="$2"
    local webhook_var="$3"
    local db_name="$4"

    local webhook_url="${!webhook_var}"
    local json_data=$(cat <<EOF
{
  "content": "<@${ADMIN_DISCORD_ID}> Database version mismatch detected!",
  "embeds": [{
    "title": "CRITICAL: Incompatible Database Version",
    "description": "Database version check failed. Service operations have been halted.",
    "color": 11141120,
    "fields": [
      {
        "name": "Database",
        "value": "$db_name",
        "inline": true
      },
      {
        "name": "Current Version",
        "value": "$version",
        "inline": true
      },
      {
        "name": "Required Version Range",
        "value": "\`$ver_range\`",
        "inline": true
      }
    ],
    "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  }]
}
EOF
)
    curl -H "Content-Type: application/json" -X POST -d "$json_data" "$webhook_url"
}


# Modified version check loop
for i in "${!ARR_WEBHOOK[@]}"; do
    webhook_var="${ARR_WEBHOOK[$i]}"
    ver_range="${ARR_VERSION[$i]}"
    db_name="${ARR_DB_NAME[$i]}"

    alembic_output=$(python3 -m alembic --name "$db_name" current -v)
    version=$(echo "$alembic_output" | grep -oP '\d+\.\d+\.\d+')

    if [ -z "$version" ]; then
        version="Not found"
        send_discord_error "$version" "$ver_range" "$webhook_var" "$db_name"
        exit 1
    fi

    is_inside_range=$(python3 "$VERSION_CHECK_FILE" "$version" "$ver_range")

    if [ "$is_inside_range" == "False" ]; then
        echo "Error: Database version $version is not within the range $ver_range."
        # Send error to Discord before exiting
        send_discord_error "$version" "$ver_range" "$webhook_var" "$db_name"
        exit 1
    fi
    echo "Database version $version is within the range $ver_range."
done
