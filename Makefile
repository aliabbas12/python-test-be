export DOCKER_BUILDKIT ?= 1

all: install
install: docker-build-backend docker-migrate-database docker-setup-superuser
run: docker-build-backend docker-migrate-database docker-run-all

# Aliases
dni: destroy install
dr: docker-run-all
drdb: docker-run-db
dm: docker-migrate-database
dmm: docker-make-migrations
dbb: docker-build-backend
dss: docker-setup-superuser
api-bash: docker-bash-into-api

# Functions / Scripts
docker-build-backend:
	$(_git_release_info)
	docker compose build api
docker-migrate-database:
	docker compose run --rm -e LOAD_ADMIN_APP=1 api python3 manage.py migrate
docker-make-migrations:
	docker compose run --rm -e LOAD_ADMIN_APP=1 api python3 manage.py makemigrations
docker-setup-superuser:
	docker compose run --rm api python3 manage.py createsuperuser --noinput
docker-bash-into-api:
	docker compose exec -it api bash
destroy:
	docker compose down -v

docker-run-all:
	docker compose up --remove-orphans

docker-run-db:
	docker compose up --remove-orphans db


define _git_release_info
	git rev-parse --abbrev-ref HEAD > ./src/menulance/runtime_helpers/git_info.txt
	git rev-parse --short=7 HEAD >> ./src/menulance/runtime_helpers/git_info.txt
endef

