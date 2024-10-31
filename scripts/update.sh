#!/bin/bash

SCRIPTS_PATH="scripts"
PROJECT_PATH="$(dirname "$SCRIPTS_PATH")"

source "$SCRIPTS_PATH/_common.sh"
loadenv

# --------------------------------------------------

VENV_ACTIVATE_PATH="$PROJECT_PATH/.venv/bin/activate"

main() {
    cd "$PROJECT_PATH" || exit

    git pull

    if [ ! -f "$VENV_ACTIVATE_PATH" ]; then
        echo "Virtual environment not found. Exiting..."
        exit 1
    fi
    source "$PROJECT_PATH/.venv/bin/activate"

    python -m alembic -n faz-cord ensure_version
    python -m alembic -n faz-wynn ensure_version
    python -m alembic -n faz-cord upgrade head
    python -m alembic -n faz-wynn upgrade head

    deactivate
}

main
