.PHONY: up down fmt lint test alembic-rev alembic-up

up:
	docker compose up -d db

down:
	docker compose down

fmt:
	poetry run black .
	poetry run ruff check . --fix

lint:
	poetry run ruff check .
	poetry run black . --check

test:
	poetry run pytest -q

alembic-rev:
	poetry run alembic revision -m "$(m)"

alembic-up:
	poetry run alembic upgrade head
