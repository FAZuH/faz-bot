DOCKER_DIR := docker
DOCKER_COMPOSE := $(DOCKER_DIR)/docker-compose.yml
SCRIPT := ./makefile.sh
.DEFAULT_GOAL := help

.PHONY: wait-for-mysql build-all up-all down-all db bot mysql pma test-sql lint test-sql-up test-sql-down lint rmpycache

help:
	@echo "Usage:"
	@echo "  make build-all							# Build all docker services"
	@echo "  make up-all 							# Up all docker services"
	@echo "  make down-all 							# Down all docker services"
	@echo "  make db act=[build|up|down|bash]		# Manage db service"
	@echo "  make bot act=[build|up|down|bash]  	# Manage bot service"
	@echo "  make mysql act=[build|up|down|bash]  	# Manage sql service"
	@echo "  make pma act=[build|up|down|bash]  	# Manage phpmyadmin service"
	@echo "  test-sql-up                    		# Up test sql container"
	@echo "  test-sql-down                  		# Down test sql container"
	@echo "  make lint					    		# Run linting"


wait-for-mysql:
	@echo "Waiting for MySQL to be ready..."
	@./$(DOCKER_DIR)/wait-for-it.sh -t 5 mysql:3306 -- echo "MySQL is ready!"

build-all:
	make sql act=build
	make wait-for-mysql
	make db act=build
	make bot act=build

up-all:
	make sql act=up
	make wait-for-mysql
	make db act=up
	make bot act=up

down-all:
	docker-compose --file $(DOCKER_COMPOSE) down


db:
	$(SCRIPT) fazdb $(act)

bot:
	$(SCRIPT) fazcord $(act)

sql:
	$(SCRIPT) mysql $(act)

test-sql:
	$(SCRIPT) test-sql $(act)

pma:
	$(SCRIPT) phpmyadmin $(act)


pytest:
	python -m pytest --disable-warnings tests

test-sql-up:
	docker run \
		--rm --name fazcord-test-db \
		-e MYSQL_ROOT_PASSWORD=password \
		-e MYSQL_USER=fazcord \
					-e MYSQL_PASSWORD=password \
		-e MYSQL_DATABASE=fazcord_test \
		-v $(PWD)/mysql/init:/docker-entrypoint-initdb.d \
		--detach --port "3306:3306" mariadb:10.5.11

test-sql-down:
	docker stop fazcord-test-db

lint:
	pylint $$(git ls-files '*.py') \
		--disable=R0801,R0901,R0913,R0916,R0912,R0902,R0914,R01702,R0917,R0904,R0911,R0915,R0903,C0301,C0114,C0115,C0116,C3001,W

rmpycache:
	find . -type d -name "__pycache__" 2> /dev/null | xargs -I {} rm -r {}
