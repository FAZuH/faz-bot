#!/bin/bash

loadenv() {
    if [ -f .env ]; then
        export $(cat .env | xargs)
    fi
}
