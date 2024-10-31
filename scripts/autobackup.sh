#!/bin/bash

SCRIPTS_PATH="scripts"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

run_backup() {
    local db_name_var="$1"
    local backup_script="$SCRIPTS_PATH/backup.sh"
    echo "Running backup for ${!db_name_var}..."
    $backup_script "backup" "$db_name_var"
}

keep_recent_backups() {
    local db_name="$1"
    local n="$2" # Number of backups to keep
    local backup_dir="$PROJECT_PATH/mysql/backup"

    mapfile -t backups < <(ls -t "$backup_dir/${db_name}_"*.sql 2>/dev/null)

    if (( ${#backups[@]} > n )); then
        for backup in "${backups[@]:n}"; do
            rm "$backup"
            echo "Deleted old backup: $backup"
        done
    else
        echo "There are $n or fewer backups, nothing to delete."
    fi
}

run() {
    local fazcord_db_name_var="MYSQL_FAZCORD_DATABASE"
    local fazwynn_db_name_var="MYSQL_FAZWYNN_DATABASE"
    echo "Starting backup process..."
    run_backup "$fazcord_db_name_var"
    run_backup "$fazwynn_db_name_var"
    keep_recent_backups "${!fazcord_db_name_var}" 3
    keep_recent_backups "${!fazwynn_db_name_var}" 3
    echo "Backup process completed."
}

main() {
    local sleep_duration="$1"
    while true; do
        run &  # run in background
        continue_time=$(date -d "+$sleep_duration seconds" +"%Y-%m-%d %H:%M:%S")
        echo "Sleeping until $continue_time..."
        sleep "$sleep_duration"
    done
}

if [ -z "${1-}" ]; then
    set -- 86400  # Default sleep duration: 1 day
fi

main "$1"
