.PHONY: install migrate collectstatic runserver test lint fix build render-start

UV := uv
MANAGE := $(UV) run python manage.py

install:
	$(UV) sync

migrate:
	$(MANAGE) migrate

collectstatic:
	$(MANAGE) collectstatic --noinput

runserver:
	@echo "Запуск сервера... (Ctrl+C для остановки)"
	$(MANAGE) runserver

test:
	$(MANAGE) test

lint:
	$(UV) run ruff check .

fix:
	$(UV) run ruff check --fix .

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi


