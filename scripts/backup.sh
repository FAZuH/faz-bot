#!/bin/bash

SCRIPTS_PATH="$(dirname "$(realpath "$0")")"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

COMMAND="$1"
DB_NAME="${!2}"  # Indirect expansion of the variable name passed as $2
BACKUP_FP="$3"

_export_backup() {
    mkdir -p "$PROJECT_PATH/mysql/backup"
    docker-compose \
        exec mysql sh -c "mariadb-dump -u root -p$MYSQL_ROOT_PASSWORD $DB_NAME" \
        > "$PROJECT_PATH/mysql/backup/${DB_NAME}_$(date +%s).sql"
}

_import_backup() {
    if [ -z "$BACKUP_FP" ]; then
        echo "Error: Backup file path is required"
        return 1
    fi
    docker-compose \
        exec -T mysql sh -c "mariadb -u root -p$MYSQL_ROOT_PASSWORD $DB_NAME" \
        < "$BACKUP_FP"
}

main() {
    source "$SCRIPTS_PATH/_common.sh"
    loadenv
    case "$COMMAND" in
        "backup") _export_backup ;;
        "load-backup") _import_backup ;;
        *)
            echo "Unknown command: $COMMAND"
            echo "Available commands: backup <db_name_var_name>, load-backup <db_name_var_name> <backup_fp>"
            exit 1
            ;;
    esac
}

main
