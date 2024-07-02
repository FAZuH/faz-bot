.PHONY: build
build: wait-for-mysql
	docker-compose --file ./docker-compose.yml up --detach --build

.PHONY: up
up: wait-for-mysql
	docker-compose --file ./docker-compose.yml up --detach

.PHONY: wait-for-mysql
wait-for-mysql:
	@echo "Waiting for MySQL to be ready..."
	@./wait-for-it.sh -t 5 mysql:3306 -- echo "MySQL is ready!"

.PHONY: down
down:
	docker-compose --file ./docker-compose.yml down


.PHONY: db-build
db-build:
	docker-compose --file ./docker-compose.yml up --detach --build faz-db

.PHONY: db-up
db-up:
	docker-compose --file ./docker-compose.yml up --detach faz-db

.PHONY: db-down
db-down:
	docker-compose --file ./docker-compose.yml down faz-db

.PHONY: db-bash
db-bash:
	docker exec -it faz-db /bin/bash

.PHONY: db
db:
	docker attach --no-stdin faz-db


.PHONY: bot-build
bot-build:
	docker-compose --file ./docker-compose.yml up --detach --build faz-bot

.PHONY: bot-up
bot-up:
	docker-compose --file ./docker-compose.yml up --detach faz-bot

.PHONY: bot-down
bot-down:
	docker-compose --file ./docker-compose.yml down faz-bot

.PHONY: bot-bash
bot-bash:
	docker exec -it bot-bash /bin/bash

.PHONY: bot
bot:
	docker attach --no-stdin faz-bot


.PHONY: sql-build
sql-build:
	docker-compose --file ./docker-compose.yml up --detach --build mysql

.PHONY: sql-up
sql-up:
	docker-compose --file ./docker-compose.yml up --detach mysql

.PHONY: sql-down
sql-down:
	docker-compose --file ./docker-compose.yml down mysql

.PHONY: sql-bash
sql-bash:
	docker exec -it mysql /bin/bash

.PHONY: sql
sql:
	docker-compose --file ./docker-compose.yml exec mysql mariadb -uroot -ppassword


.PHONY: pma-up
pma-up:
	docker-compose --file ./docker-compose.yml up --detach phpmyadmin

.PHONY: pma-down
pma-down:
	docker-compose --file ./docker-compose.yml down phpmyadmin



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



.PHONY: lint
lint:
	pylint fazbot\ --disable=R0901,R0913,R0916,R0912,R0902,R0914,R01702,R0917,R0904,R0911,R0915,R0903,C0301,C0114,C0115,C0116,W
