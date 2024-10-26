#!/bin/bash

projectDir=$(dirname "$(dirname "$(realpath "$0")")")
cd "$projectDir" || exit

echo "Pulling latest git commit in $projectDir..."
git pull origin main

echo "Running update script..."
UPDATE_SCRIPT="$projectDir/scripts/update.sh"

$UPDATE_SCRIPT
