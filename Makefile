.PHONY: down build migrate superuser env

env:
ifeq ($(OS),Windows_NT)
	copy backend\.env.example backend\.env
else
	cp backend/.env.example backend/.env
endif

down:
	docker-compose down -v

build:
	docker-compose up -d --build

migrate:
	docker-compose exec api python manage.py makemigrations
	docker-compose exec api python manage.py migrate

superuser:
	docker-compose exec api python manage.py createsuperuser