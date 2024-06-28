.PHONY: build
build:
	docker-compose -f ./docker-compose.yml up --detach --build

.PHONY: up
up:
	docker-compose -f ./docker-compose.yml up --detach

.PHONY: down
down:
	docker-compose -f ./docker-compose.yml down

.PHONY: sql
sql:
	docker-compose -f ./docker-compose.yml exec mysql mariadb -uroot -ppassword fazbot


.PHONY: db-up
db-up:
	docker-compose --file ./docker-compose.yml up --detach faz-db

.PHONY: db-down
db-down:
	docker-compose --file ./docker-compose.yml down faz-db

.PHONY: bot-up
bot-up:
	docker-compose --file ./docker-compose.yml up --detach faz-bot

.PHONY: bot-down
bot-down:
	docker-compose --file ./docker-compose.yml down faz-bot

.PHONY: sql-up
sql-up:
	docker-compose --file ./docker-compose.yml up --detach mysql

.PHONY: sql-down
sql-down:
	docker-compose --file ./docker-compose.yml down mysql


.PHONY: test-sql-up
test-sql-up:
	docker run \
			--rm --name fazbot-test-db \
            -e MYSQL_ROOT_PASSWORD=password \
            -e MYSQL_USER=fazbot \
						-e MYSQL_PASSWORD=password \
            -e MYSQL_DATABASE=fazbot_test \
            -v $(PWD)/mysql/init:/docker-entrypoint-initdb.d \
            --detach --port "3306:3306" mariadb:10.5.11

.PHONY: test-sql-down
test-sql-down:
	docker stop fazbot-test-db



.PHONY: run
run:
	source .venv/bin/activate
	python -m fazbot

.PHONY: install
install:
	python3.12 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	cp .env-example .env

.PHONY: lint
lint:
	pylint fazbot\ --disable=R0901,R0913,R0916,R0912,R0902,R0914,R01702,R0917,R0904,R0911,R0915,R0903,C0301,C0114,C0115,C0116,W
