MANAGE := poetry run python manage.py

install:
	poetry install

migrate:
	${MANAGE} makemigrations
	${MANAGE} migrate

build: install migrate

lint:
	poetry run flake8 task_manager --exclude migrations

test:
	${MANAGE} test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

selfcheck:
	poetry check

check: selfcheck test-coverage lint

shell:
	${MANAGE} shell_plus --ipython

dev:
	${MANAGE} runserver

start:
	poetry run gunicorn task_manager.wsgi

trans:
	poetry run django-admin makemessages --ignore="static" --ignore=".env" -l ru

compile:
	poetry run django-admin compilemessages


.PHONY: install test lint selfcheck check task_manager