DOCKER_DIR := docker
DOCKER_COMPOSE := $(DOCKER_DIR)/docker-compose.yml
SCRIPT := ./makefile.sh
.DEFAULT_GOAL := help

.PHONY: wait-for-mysql build-all up-all down-all db bot mysql pma test-sql lint test-sql-up test-sql-down lint

help:
	@echo "Usage:"
	@echo "  make build-all						# Build all docker services"
	@echo "  make up-all 						# Up all docker services"
	@echo "  make down-all 						# Down all docker services"
	@echo "  make db [build|up|down|bash]		# Manage db service"
	@echo "  make bot [build|up|down|bash]  	# Manage bot service"
	@echo "  make mysql [build|up|down|bash]  	# Manage sql service"
	@echo "  make pma [build|up|down|bash]  	# Manage phpmyadmin service"
	@echo "  test-sql-up                    	# Up test sql container"
	@echo "  test-sql-down                  	# Down test sql container"
	@echo "  make lint					    	# Run linting"


wait-for-mysql:
	@echo "Waiting for MySQL to be ready..."
	@./$(DOCKER_DIR)/wait-for-it.sh -t 5 mysql:3306 -- echo "MySQL is ready!"

build-all:
	make sql build
	make wait-for-mysql
	make db build
	make bot build

up-all:
	make sql up
	make wait-for-mysql
	make db up
	make bot up

down-all:
	docker-compose --file $(DOCKER_COMPOSE) down


db:
	$(SCRIPT) fazdb $(word 2,$(MAKECMDGOALS))

bot:
	$(SCRIPT) fazbot $(word 2,$(MAKECMDGOALS))

sql:
	$(SCRIPT) mysql $(word 2,$(MAKECMDGOALS))

test-sql:
	$(SCRIPT) test-sql $(word 2,$(MAKECMDGOALS))

pma:
	$(SCRIPT) pma $(word 2,$(MAKECMDGOALS))


test-sql-up:
	docker run \
		--rm --name fazbot-test-db \
		-e MYSQL_ROOT_PASSWORD=password \
		-e MYSQL_USER=fazbot \
					-e MYSQL_PASSWORD=password \
		-e MYSQL_DATABASE=fazbot_test \
		-v $(PWD)/mysql/init:/docker-entrypoint-initdb.d \
		--detach --port "3306:3306" mariadb:10.5.11

test-sql-down:
	docker stop fazbot-test-db

lint:
	pylint fazbot \
		--disable=R0901,R0913,R0916,R0912,R0902,R0914,R01702,R0917,R0904,R0911,R0915,R0903,C0301,C0114,C0115,C0116,W
