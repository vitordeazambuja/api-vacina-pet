.PHONY: up down build logs migrate superuser

up:
	docker-compose up -d

down:
	docker-compose down -v

build:
	docker-compose up -d --build

migrate:
	docker-compose exec api python manage.py makemigrations
	docker-compose exec api python manage.py migrate

superuser:
	docker-compose exec api python manage.py createsuperuser