#!/bin/bash

echo "Pulling latest git commit..."
git pull origin main

scrDir=$(dirname "$(realpath "$0")")

echo "Running update script..."
UPDATE_SCRIPT="$scrDir/../docker/update.sh"

$UPDATE_SCRIPT
