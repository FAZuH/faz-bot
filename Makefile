ifneq (,$(wildcard ./.env))
    include .env
    export
endif

DOCKER_DIR := docker
SCRIPTS_DIR := scripts
SERVICESCRIPT := $(SCRIPTS_DIR)/service.sh
BACKUPSCRIPT := $(SCRIPTS_DIR)/backup.sh

PYTHON := python

.DEFAULT_GOAL := help

.PHONY: wait-for-mysql build-all up-all down-all api_collect bot mysql pma test lint lint-fix format rmpycache countlines clean backup

help:
	@echo "Usage:"
	@echo "  make init                                  	# Initialize project"
	@echo "  make build-all                             	# Build all docker services"
	@echo "  make up-all                                	# Up all docker services"
	@echo "  make down-all                              	# Down all docker services"
	@echo "  make api_collect act=[pull|build|up|down|bash] # Manage api_collect service"
	@echo "  make bot act=[pull|build|up|down|bash]         # Manage bot service"
	@echo "  make sql act=[pull|build|up|down|bash]         # Manage sql service"
	@echo "  make pma act=[pull|build|up|down|bash]         # Manage phpmyadmin service"
	@echo "  make test                                  	# Run python tests"
	@echo "  make lint-fix                              	# Run python linting with Ruff with --fix on"
	@echo "  make format                                	# Run python formatting with Black"
	@echo "  make rmpycache                             	# Remove __pycache__ directories"
	@echo "  make countlines                            	# Count sum of lines of all python files"
	@echo "  make clean                                 	# Lint, format, test, and rmpycache"
	@echo "  make backup-fazcord                          	# Backup faz-cord database"
	@echo "  make backup-fazdb                          	# Backup faz-db database"
	@echo "  make load-backup-fazcord path=<path>           # Load faz-cord database from a .sql backup file"
	@echo "  make load-backup-fazdb path=<path>             # Load faz-db database from a .sql backup file"


init:
	@echo "Initializing..."
	cp .env-example .env
	$(PYTHON) -m venv .venv && source .venv/bin/activate && pip install alembic pymysql sortedcontainers
	@echo "Done!"

initdb:
	@echo "Initializing database..."
	source .venv/bin/activate && ./scripts/initdb.sh $(PYTHON)
	@echo "Done!"

wait-for-mysql:
	@echo "Waiting for MySQL to be ready..."
	$(DOCKER_DIR)/wait-for-it.sh -t 5 mysql:3306 -- echo "MySQL is ready!"

build-all:
	make sql act=build
	make wait-for-mysql
	make api_collect act=build
	make bot act=build

up-all:
	make sql act=up
	make wait-for-mysql
	make api_collect act=up
	make bot act=up

down-all:
	docker-compose down


api_collect:
	$(SERVICESCRIPT) api_collect $(act)

bot:
	$(SERVICESCRIPT) fazcord $(act)

sql:
	$(SERVICESCRIPT) mysql $(act)

# test-sql:
# 	$(SERVICESCRIPT) test-sql $(act)

pma:
	$(SERVICESCRIPT) phpmyadmin $(act)


test:
	$(PYTHON) -m pytest --disable-warnings tests/

lint-fix:
	$(PYTHON) -m ruff check --fix .

format:
	$(PYTHON) -m black .


rmpycache:
	find . -type d -name "__pycache__" 2> /dev/null | xargs -I {} rm -r {}

countlines:
	find . -name "*.py" -type f -exec wc -l {} + | sort -n


clean:
	make lint-fix
	make format
	make test
	make rmpycache


backup-fazcord:
	$(BACKUPSCRIPT) backup MYSQL_FAZCORD_DATABASE

backup-fazdb:
	$(BACKUPSCRIPT) backup MYSQL_FAZDB_DATABASE

load-backup-fazcord:
	$(BACKUPSCRIPT) load-backup MYSQL_FAZCORD_DATABASE $(path)

load-backup-fazdb:
	$(BACKUPSCRIPT) load-backup MYSQL_FAZDB_DATABASE $(path)


reset-docker:
	docker stop $$(docker ps -aq)
	docker rm $$(docker ps -aq)
	docker rmi $$(docker images -q)
	docker volume prune -f
	docker builder prune -f
	docker network rm $$(docker network ls -q)
