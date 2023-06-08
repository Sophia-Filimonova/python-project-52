install:
	poetry install

lint:
	poetry run flake8 page_analyzer

selfcheck:
	poetry check

check: selfcheck lint

dev:
	poetry run python manage.py runserver

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

.PHONY: install test lint selfcheck check page_analyzer build