CURRENT_DIR := $(shell pwd)
ENVIRONMENT := $(shell grep ENVIRONMENT .env | cut -d= -f2 | tr -d "'")

.PHONY: help start stop logs restart rebuild clean db-logs db-root db-bash

help:
	@echo "MovieProphet - Available Commands:"
	@echo "  make start      - Stop existing containers, build and start all services"
	@echo "  make stop       - Stop and remove all containers"
	@echo "  make logs       - Follow application logs"
	@echo "  make restart    - Restart all services"
	@echo "  make rebuild    - Force rebuild and restart all services"
	@echo "  make clean      - Stop containers and remove volumes (data will be lost)"
	@echo "  make shell-app  - Open shell in the Flask app container"
	@echo "  make shell-db   - Open MySQL shell (as movieprophet_user)"
	@echo "  make db-root    - Open MySQL shell as root user"
	@echo "  make db-logs    - Show MySQL container logs"

start: stop
	docker-compose up --build -d
	@echo "Waiting for services to be ready..."
	@sleep 5
	docker logs --follow movieprophet_app

stop:
	-docker stop movieprophet_app
	-docker stop movieprophet_mysql
	-docker rm movieprophet_app
	-docker rm movieprophet_mysql

logs:
	docker logs --follow movieprophet_app

restart: stop start

rebuild:
	docker-compose up --build --force-recreate -d
	docker logs --follow movieprophet_app

clean: stop
	-docker volume rm movieprophet_mysql-data
	-rm -rf mysql/data
	@echo "All containers and volumes removed"

shell-app:
	docker exec -it movieprophet_app /bin/bash

shell-db:
	docker exec -it movieprophet_mysql mysql -u$(shell grep MYSQL_USER .env | cut -d= -f2 | tr -d "'") -p$(shell grep MYSQL_PASSWORD .env | cut -d= -f2 | tr -d "'") $(shell grep MYSQL_DATABASE .env | cut -d= -f2 | tr -d "'")

db-root:
	docker exec -it movieprophet_mysql mysql -uroot -p$(shell grep MYSQL_ROOT_PASSWORD .env | cut -d= -f2 | tr -d "'")

db-logs:
	docker logs movieprophet_mysql
