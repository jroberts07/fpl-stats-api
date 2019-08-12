NAME = fantasy_api
COMPOSE_FILE = src/docker-compose.yml

help:
	@perl -ne 'print if /^[0-9a-zA-Z_-]+:.*?## .*$$/' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

env-compose:
	$(eval export COMPOSE_FILE=$(COMPOSE_FILE))

build: env-compose ## Builds the docker image to run the app
	@docker-compose build

run: env-compose ## Runs the code in a container
	@docker-compose up -d fantasy_api

stop: env-compose ## Stop the services required for the dev environment.
	@docker-compose stop

test: env-compose ## Runs the unit tests
	@docker-compose run --rm fantasy_api_test

logs: env-compose ## Logs
	@docker-compose logs --tail=500 -f fantasy_api

shell: env-compose ## Shell into main container
	@docker-compose exec fantasy_api sh

down: env-compose ## Stop the services and remove containers and volumes
	@docker-compose down --volumes

clean: env-compose ## Stop the services and remove containers, volumes and docker images
	@docker-compose down --volumes --rmi all

ps: env-compose ## View current running containers
	@docker-compose ps

.PHONY: help env-compose build run stop logs shell down clean ps