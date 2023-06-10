install:
	poetry install

lint:
	poetry run flake8 task_manager

selfcheck:
	poetry check

check: selfcheck lint

dev:
	poetry run python manage.py runserver

start:
	poetry run gunicorn task_manager.wsgi

trans:
	poetry run django-admin makemessages --ignore="static" --ignore=".env" -l ru

compile:
	poetry run django-admin compilemessages

.PHONY: install test lint selfcheck check task_manager