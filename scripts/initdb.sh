#!/bin/bash
set -euo pipefail

SCRIPTS_PATH="$(dirname "$(realpath "$0")")"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

checkenv

validate_db_name() {
    local db_name="$1"
    if [[ ! "$db_name" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        echo "Error: Invalid database name: $db_name"
        exit 1
    fi
}

run_sql() {
    local command="$1"
    if ! $COMPOSE exec -i mysql mariadb -u root \
        -p"$MYSQL_ROOT_PASSWORD" -h "$MYSQL_HOST" -P "$MYSQL_PORT" \
        -e "$command"; then
        echo "Error: Failed to execute SQL command"
        exit 1
    fi
}

create_db() {
    local db_name="$1"
    local db_name_test="$db_name""_test"
    validate_db_name "$db_name"
    echo "Creating database: $db_name and $db_name_test"
    run_sql "CREATE DATABASE IF NOT EXISTS \`$db_name\`;"
    run_sql "CREATE DATABASE IF NOT EXISTS \`$db_name_test\`;"
}

grant_privilege() { local db_name="$1"
    local db_name_test="$db_name""_test"
    validate_db_name "$db_name"
    echo "Granting privileges on $db_name and $db_name_test to $MYSQL_USER"
    run_sql "GRANT ALL PRIVILEGES ON \`$db_name\`.* TO '$MYSQL_USER'@'%';"
    run_sql "GRANT ALL PRIVILEGES ON \`$db_name_test\`.* TO '$MYSQL_USER'@'%';"
}

create_user() {
    echo "Creating user: $MYSQL_USER"
    run_sql "CREATE USER IF NOT EXISTS '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';"
}

create_dbs() {
    create_db "$MYSQL_FAZDB_DATABASE"
    create_db "$MYSQL_FAZCORD_DATABASE"
}

grant_privileges() {
    grant_privilege "$MYSQL_FAZDB_DATABASE"
    grant_privilege "$MYSQL_FAZCORD_DATABASE"
    run_sql "FLUSH PRIVILEGES;"
}

check_alembic() {
    local python_bin="$1"
    if ! $python_bin -c "import alembic" 2>/dev/null; then
        echo "Error: alembic Python module not found. Install it with 'pip install alembic'"
        exit 1
    fi
}

init_db() {
    local python_bin="$1"
    local name="$2"
    local name_test="$name""_test"
    $python_bin -m alembic -n "$name" ensure_version
    $python_bin -m alembic -n "$name" upgrade head
    $python_bin -m alembic -n "$name_test" ensure_version
    $python_bin -m alembic -n "$name_test" upgrade head
}

init_dbs() {
    local python_bin="$1"
    init_db "$python_bin" "faz-db" 
    init_db "$python_bin" "faz-cord" 
}


main() {
    local python_bin="$1"
    check_alembic "$1"
    echo "Starting database setup..."
    create_user
    create_dbs
    grant_privileges
    init_dbs "$1"
    echo "Database setup completed successfully"
}

# Trap errors
trap 'echo "Error: Script failed on line $LINENO"' ERR

if [ -z "${1-}" ]; then
    set -- "python"
fi

main "$1"
