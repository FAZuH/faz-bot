DOCKER_DIR := docker
DOCKER_COMPOSE := $(DOCKER_DIR)/docker-compose.yml
SCRIPT := ./makefile.sh
.DEFAULT_GOAL := help

.PHONY: wait-for-mysql build-all up-all down-all api-collect bot mysql pma test lint format rmpycache countlines

help:
	@echo "Usage:"
	@echo "  make build-all                             # Build all docker services"
	@echo "  make up-all                                # Up all docker services"
	@echo "  make down-all                              # Down all docker services"
	@echo "  make api-collect act=[build|up|down|bash]  # Manage api-collect service"
	@echo "  make bot act=[build|up|down|bash]          # Manage bot service"
	@echo "  make sql act=[build|up|down|bash]          # Manage sql service"
	@echo "  make pma act=[build|up|down|bash]          # Manage phpmyadmin service"
	@echo "  make test                                  # Run python tests"
	@echo "  make lint                                  # Run python linting"
	@echo "  make format                                # Run python formatting with isort and black"
	@echo "  make rmpycache                             # Remove __pycache__ directories"
	@echo "  make countlines                            # Count sum of lines of all python files"


wait-for-mysql:
	@echo "Waiting for MySQL to be ready..."
	@./$(DOCKER_DIR)/wait-for-it.sh -t 5 mysql:3306 -- echo "MySQL is ready!"

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
	docker-compose --file $(DOCKER_COMPOSE) down


api-collect:
	$(SCRIPT) api_collect $(act)

bot:
	$(SCRIPT) fazcord $(act)

sql:
	$(SCRIPT) mysql $(act)

# test-sql:
# 	$(SCRIPT) test-sql $(act)

pma:
	$(SCRIPT) phpmyadmin $(act)


test:
	python -m pytest --disable-warnings tests

lint:
	python -m pylint $$(git ls-files '*.py') --disable=R0801,R0901,R0913,R0916,R0912,R0902,R0914,R01702,R0917,R0904,R0911,R0915,R0903,C0301,C0114,C0115,C0116,C3001,W

format:
	python -m isort . && python -m black .


rmpycache:
	find . -type d -name "__pycache__" 2> /dev/null | xargs -I {} rm -r {}

countlines:
	find . -name '*.py' -type f -exec wc -l {} + | awk '{total += $1} END {print "Total lines in all .py files:", total}'


clean:
	make rmpycache
	make format
	make test
	make lint
