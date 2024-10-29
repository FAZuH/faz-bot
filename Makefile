DOCKER_DIR := docker
SCRIPTS_DIR := scripts
MAKESCRIPT := $(SCRIPTS_DIR)/service.sh
.DEFAULT_GOAL := help

.PHONY: wait-for-mysql build-all up-all down-all api-collect bot mysql pma test lint lint-fix format rmpycache countlines clean backup

help:
	@echo "Usage:"
	@echo "  make build-all                             	# Build all docker services"
	@echo "  make up-all                                	# Up all docker services"
	@echo "  make down-all                              	# Down all docker services"
	@echo "  make api-collect act=[pull|build|up|down|bash] # Manage api-collect service"
	@echo "  make bot act=[pull|build|up|down|bash]         # Manage bot service"
	@echo "  make sql act=[pull|build|up|down|bash]         # Manage sql service"
	@echo "  make pma act=[pull|build|up|down|bash]         # Manage phpmyadmin service"
	@echo "  make test                                  	# Run python tests"
	@echo "  make lint                                  	# Run python linting with Ruff"
	@echo "  make lint-fix                              	# Run python linting with Ruff with --fix on"
	@echo "  make format                                	# Run python formatting with Black"
	@echo "  make rmpycache                             	# Remove __pycache__ directories"
	@echo "  make countlines                            	# Count sum of lines of all python files"
	@echo "  make clean                                 	# Lint, format, test, and rmpycache"
	@echo "  make backup                                 	# Backup faz-cord and faz-db databases"
	@echo "  make load-backup-fazdb path=<path>             # Load faz-db database from a .sql backup file"
	@echo "  make load-backup-fazcord path=<path>           # Load faz-cord database from a .sql backup file"


init:
	@echo "Initializing..."
	cp .env.example .env
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements-dev.txt
	python -m alembic -n api_collect ensure_version
	python -m alembic -n fazcord ensure_version
	@echo "Done!"

wait-for-mysql:
	@echo "Waiting for MySQL to be ready..."
	./$(DOCKER_DIR)/wait-for-it.sh -t 5 mysql:3306 -- echo "MySQL is ready!"

build-all:
	make sql act=build
	make wait-for-mysql
	make api-collect act=build
	make bot act=build

up-all:
	make sql act=up
	make wait-for-mysql
	make api-collect act=up
	make bot act=up

down-all:
	docker-compose down


api-collect:
	$(MAKESCRIPT) api_collect $(act)

bot:
	$(MAKESCRIPT) fazcord $(act)

sql:
	$(MAKESCRIPT) mysql $(act)

# test-sql:
# 	$(MAKESCRIPT) test-sql $(act)

pma:
	$(MAKESCRIPT) phpmyadmin $(act)


test:
	python -m pytest --disable-warnings tests/

lint:
	python -m ruff check .

lint-fix:
	python -m ruff check --fix .

format:
	python -m black .


rmpycache:
	find . -type d -name "__pycache__" 2> /dev/null | xargs -I {} rm -r {}

countlines:
	find . -name "*.py" -type f -exec wc -l {} + | sort -n


clean:
	@make lint-fix
	@make format
	@make test
	@make rmpycache


backup:
	mkdir -p mysql/backup
	docker-compose \
		exec mysql sh -c 'mariadb-dump -u root -p$$MYSQL_ROOT_PASSWORD faz-cord' \
		> mysql/backup/faz-cord_`date +%s`.sql
	docker-compose \
		exec mysql sh -c 'mariadb-dump -u root -p$$MYSQL_ROOT_PASSWORD faz-db' \
		> mysql/backup/faz-db_`date +%s`.sql

load-backup-fazcord:
	docker-compose \
		exec -T mysql sh -c 'mariadb -u root -p"$$MYSQL_ROOT_PASSWORD" faz-cord' \
		< $(path)

load-backup-fazdb:
	docker-compose \
		exec -T mysql sh -c 'mariadb -u root -p"$$MYSQL_ROOT_PASSWORD" faz-db' \
		< $(path)


reset-docker:
	docker stop $$(docker ps -aq)
	docker rm $$(docker ps -aq)
	docker rmi $$(docker images -q)
	docker volume prune -f
	docker builder prune -f
	docker network rm $$(docker network ls -q)
