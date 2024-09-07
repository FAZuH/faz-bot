#!/bin/bash

scrDir=$(dirname "$(realpath "$0")")

cd "$scrDir" || exit

echo "Pulling latest git commit in $scrDir..."
git pull origin main

echo "Running update script..."
UPDATE_SCRIPT="$scrDir/../docker/update.sh"

$UPDATE_SCRIPT
