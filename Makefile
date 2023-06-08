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

.PHONY: install test lint selfcheck check task_manager